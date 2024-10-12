from django.views import View
from django.shortcuts import render
from django.db.models import Q, Prefetch
from .forms import WordSearchForm
from django.contrib.auth import get_user_model
from users.models import Deck, WordPerformance, UserDeck
from chineseword.models import ChineseWord
from .forms import SearchForm
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.db.models import F, ExpressionWrapper, FloatField
from django.core.cache import cache

User = get_user_model()

class CurrentUserMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context

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
        """Fetch the latest 4 decks for the user and return Deck instances with UserDeck data."""
        user_decks = user.userdeck_set.all()
        return Deck.objects.prefetch_related(
            Prefetch('userdeck_set',
                     queryset=user_decks.filter(user=user),
                     to_attr='user_deck')
        ).filter(creator=user).order_by('-userdeck__edited')[:4]

    def get_context_data(self, user):
        """Build the context data to pass to the template."""
        context = {
            'perform': self.get_performances(user),
            'current_user': user,
            'recent_decks': self.get_recent_decks(user),
        }
        return context


class UserDecksView(LoginRequiredMixin, CurrentUserMixin, ListView):
    model = UserDeck
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
        """Get the decks related to the user and order them by the UserDeck timestamp."""
        return Deck.objects.filter(users=user).prefetch_related(
            Prefetch(
                'userdeck_set',
                queryset=UserDeck.objects.filter(user=user).only('id', 'percent', 'deck_id', 'timestamp'),
                to_attr='user_deck'
            )
        ).order_by('-userdeck__timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['current_user'] = self.request.user
        return context


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


class AllWordsView(WordPaginationMixin, CurrentUserMixin, ListView):
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

class WordFilteringMixin:
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
        elif review_period == '':
            queryset = queryset
        elif review_period == 'zero':
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
        # Annotate the queryset with `accuracy_percentage`
        queryset = queryset.annotate(
            accuracy_percentage=ExpressionWrapper(
                (F('right') * 100.0) / (F('right') + F('wrong')),
                output_field=FloatField()
            )
        )

        if sort_by == 'accuracy_percentage':
            return queryset.order_by(sort_order == 'asc' and 'accuracy_percentage' or '-accuracy_percentage')

        return queryset.order_by(sort_order == 'asc' and sort_by or f'-{sort_by}')

    def apply_search_filter(self, queryset):
        """Apply the search filter if a search query is provided."""
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(word__simplified__icontains=search_query) |
                Q(word__traditional__icontains=search_query) |
                Q(word__pinyin__icontains=search_query) |
                Q(word__meaning__icontains=search_query)
            )
        return queryset


class UserWordsView(LoginRequiredMixin, CurrentUserMixin, WordFilteringMixin, WordPaginationMixin, ListView):
    model = WordPerformance
    template_name = 'mywords.html'
    context_object_name = 'performances'

    def get_queryset(self):
        # Start with the queryset for the logged-in user
        queryset = WordPerformance.objects.filter(user=self.request.user).select_related('word')

        # Apply filters
        queryset = self.apply_search_filter(queryset)
        queryset = self.apply_review_period_filter(queryset)
        queryset = self.apply_hsk_level_filter(queryset)
        queryset = self.apply_sorting(queryset)

        return queryset  # Return the filtered and paginated queryset

    def get_context_data(self, **kwargs):
        """Add additional context to the template."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        context['review_period'] = self.request.GET.get('review_period', '')
        context['now'] = timezone.now()
        total_performances_count = self.get_queryset().count()
        context['total_performances_count'] = total_performances_count
        return context

class ReviewWordsView(CurrentUserMixin, WordFilteringMixin, ListView):
    model = WordPerformance
    template_name = 'review_words.html'
    context_object_name = 'performances'

    def get_queryset(self):
        # Start with the queryset for the logged-in user
        queryset = WordPerformance.objects.filter(user=self.request.user).select_related('word')

        # Apply filters
        queryset = self.apply_search_filter(queryset)
        queryset = self.apply_review_period_filter(queryset)
        queryset = self.apply_hsk_level_filter(queryset)
        queryset = self.apply_sorting(queryset)

        return queryset  # Return the filtered queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        review_period = self.request.GET.get('review_period', '')
        hsk_levels = self.request.GET.getlist('hsk_levels')

        context['period'], context['hsk_levels'] = translate_to_russian(review_period, hsk_levels)
        context['to_test'] = self.filter_due_words(self.get_queryset())
        return context

    def filter_due_words(self, queryset):
        """Filter words that are due for review based on next_review_date."""
        now = timezone.now()
        # Filter the queryset directly
        due_words = queryset.filter(next_review_date__lte=now)

        # Returning a list of dictionaries containing word and performance
        return [
            {
                'word': performance.word,  # Use the related `word`
                'performance': performance
            }
            for performance in due_words
        ]

def translate_to_russian(review_period=None, hsk_levels=None):
    """Transform review period and HSK levels to Russian verbose names."""
    review_period_mapping = {
        'last_week': 'Последняя неделя',
        'last_three_days': 'Последние три дня',
        'last_day': 'Последний день',
        'zero': 'Нет повторений',
        'three_days': 'Три дня',
        'week': 'Неделя',
    }

    hsk_level_mapping = {
        '1': 'HSK 1',
        '2': 'HSK 2',
        '3': 'HSK 3',
        '4': 'HSK 4',
        '5': 'HSK 5',
        '6': 'HSK 6',
    }

    translated_period = review_period_mapping.get(review_period, review_period)
    translated_levels = [hsk_level_mapping.get(level, level) for level in hsk_levels] if hsk_levels else []

    return translated_period, translated_levels
