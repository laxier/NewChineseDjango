from django.views import View
from django.shortcuts import render
from django.db.models import Q, Prefetch
from .forms import WordSearchForm
from django.contrib.auth import get_user_model
from users.models import Deck, WordPerformance
from chineseword.models import ChineseWord
from .forms import SearchForm
from django.utils import timezone
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.core.paginator import Paginator


class IndexPageView(LoginRequiredMixin, View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        current_user = request.user
        context = self.get_context_data(current_user)
        return render(request, self.template_name, context)

    def get_performances(self, user):
        """Fetch the latest 5 word performances for the user."""
        return (
            WordPerformance.objects.filter(user=user)
            .prefetch_related(
                Prefetch('word', queryset=ChineseWord.objects.all())
            )
            .order_by('-timestamp')
            [:5]
        )

    def get_recent_decks(self, user):
        """Fetch the latest 4 decks for the user."""
        return user.decks.all().order_by('name')[:4]

    def get_context_data(self, user):
        """Build the context data to pass to the template."""
        context = {
            'perform': self.get_performances(user),
            'current_user': user,
            'recent_decks': self.get_recent_decks(user),
        }
        return context


User = get_user_model()


class UserDecksView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = 'decks.html'
    context_object_name = 'decks'
    paginate_by = 20

    def get_queryset(self):
        self.user = self.get_user()
        return self.get_user_decks(self.user)

    def get_user(self):
        """Retrieve the user object based on the provided username."""
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_user_decks(self, user):
        """Get the decks related to the user and order them by ID."""
        return Deck.objects.filter(users=user).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['current_user'] = self.request.user
        return context


class SearchFilterMixin:
    """
    Mixin to provide search filtering functionality for ListViews.
    This mixin expects the model to have 'simplified', 'traditional', 'pinyin', and 'meaning' fields.
    """

    def apply_search_filter(self, queryset):
        """Apply the search filter if a search query is provided."""
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(simplified__icontains=search_query) |
                Q(traditional__icontains=search_query) |
                Q(pinyin__icontains=search_query) |
                Q(meaning__icontains=search_query)
            )
        return queryset


class WordPaginationMixin:
    """
    Mixin to provide pagination functionality for word-related views.
    This mixin adds pagination capabilities to ListViews.
    """
    paginate_by = 20  # Default number of items per page

    def get_paginated_queryset(self, queryset):
        """Paginate the queryset based on the current page number."""
        page_number = self.request.GET.get('page', 1)  # Default to the first page
        paginator = Paginator(queryset, self.paginate_by)
        page_obj = paginator.get_page(page_number)
        return page_obj


class AllWordsView(SearchFilterMixin, WordPaginationMixin, ListView):
    template_name = 'all_words.html'
    context_object_name = 'words'

    def get_queryset(self):
        queryset = self.get_base_queryset()

        if self.request.user.is_authenticated:
            queryset = self.prefetch_user_performance(queryset)

        queryset = self.apply_search_filter(queryset)
        return queryset

    def get_base_queryset(self):
        """Retrieve the base queryset for all words that have meanings."""
        return ChineseWord.objects.filter(meaning__isnull=False).order_by('simplified')

    def prefetch_user_performance(self, queryset):
        """Prefetch the user's performance on words."""
        return queryset.prefetch_related(
            Prefetch('performance',
                     queryset=WordPerformance.objects.filter(user=self.request.user),
                     to_attr='user_performance')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все слова'
        context['search_form'] = WordSearchForm(self.request.GET)
        context['current_user'] = self.request.user

        # Add user performance context
        if self.request.user.is_authenticated:
            context['performances'] = {word.id: word.user_performance for word in self.object_list}
        else:
            context['performances'] = None  # or an empty dictionary if you prefer

        return context


class UserWordsView(LoginRequiredMixin, SearchFilterMixin, WordPaginationMixin, ListView):
    model = WordPerformance
    template_name = 'mywords.html'
    context_object_name = 'performances'

    def get_queryset(self):
        performances = WordPerformance.objects.filter(user=self.request.user).select_related('word')

        performances = self.apply_search_filter(performances)
        performances = self.apply_review_period_filter(performances)
        performances = self.apply_hsk_level_filter(performances)
        performances = self.apply_sorting(performances)

        return performances

    def apply_review_period_filter(self, queryset):
        """Applies filtering based on the selected review period."""
        review_period = self.request.GET.get('review_period', '')
        now = timezone.now()

        if review_period == 'last_week':
            queryset = queryset.filter(next_review_date__gte=now - timedelta(days=7), next_review_date__lte=now)
        elif review_period == 'last_three_days':
            queryset = queryset.filter(next_review_date__gte=now - timedelta(days=3), next_review_date__lte=now)
        elif review_period == 'last_day':
            queryset = queryset.filter(next_review_date__gte=now - timedelta(days=1), next_review_date__lte=now)
        elif review_period in ['', 'zero']:
            queryset = queryset.filter(next_review_date__gte=now)
        elif review_period == 'three_days':
            queryset = queryset.filter(next_review_date__lte=now + timedelta(days=3), next_review_date__gte=now)
        elif review_period == 'week':
            queryset = queryset.filter(next_review_date__lte=now + timedelta(days=7), next_review_date__gte=now)

        return queryset

    def apply_hsk_level_filter(self, queryset):
        """Applies filtering based on HSK levels."""
        hsk_levels = self.request.GET.getlist('hsk_levels')
        if hsk_levels:
            queryset = queryset.filter(word__hsk_level__in=hsk_levels)
        return queryset

    def apply_sorting(self, queryset):
        """Applies sorting based on query parameters."""
        sort_by = self.request.GET.get('sort_by', 'edited')
        sort_order = self.request.GET.get('sort_order', 'desc')

        if sort_order == 'asc':
            return queryset.order_by(sort_by)
        return queryset.order_by(f'-{sort_by}')

    def get_context_data(self, **kwargs):
        """Add additional context to the template."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        context['review_period'] = self.request.GET.get('review_period', '')
        context['now'] = timezone.now()
        context['current_user'] = self.request.user
        return context

class DeckDetailView(DetailView):
    model = Deck
    template_name = 'deck_detail.html'
    context_object_name = 'deck'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck = self.object
        current_user = self.request.user

        context['current_user'] = current_user
        words_in_deck = deck.words.all()
        if current_user.is_authenticated:
            performances = WordPerformance.objects.filter(word__in=words_in_deck, user=current_user)
            context['performances'] = performances
            context['deck_data'] = self.get_performance_data(deck, performances)
        else:
            context['words'] = words_in_deck

        return context

    def get_performance_data(self, deck, user):
        return {
            "dates": [],  # Dates for performance data
            "percentages": [],  # Percentages of correct answers
            "wrongAnswers": [],  # Array of wrong answers
            "id": []  # IDs corresponding to performance data
        }

    def get_queryset(self):
        return Deck.objects.prefetch_related('words')


from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView

class EditDeckView(UpdateView):
    pass
class ReviewDeckView(ListView):
    pass

class TestDeckView(ListView):
    pass

class AddDeckView(CreateView):
    pass
