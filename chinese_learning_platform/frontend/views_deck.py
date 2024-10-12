from django.views.generic import UpdateView, CreateView, ListView, DetailView
from django.urls import reverse_lazy
from users.models import Deck, WordPerformance, DeckPerformance, DeckWord
from chineseword.models import ChineseWord
from .forms_deck import WordForm
from django.contrib import messages
import re
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Prefetch

class CurrentUserMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context


class CurrentDateTimeMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class DeckDetailView(CurrentUserMixin, CurrentDateTimeMixin, DetailView):
    model = Deck
    template_name = 'deck_detail.html'
    context_object_name = 'deck'

    def get_queryset(self):
        """
        Prefetch words and their related performances for the current user using a 'double index'.
        This method retrieves Deck -> Words -> Performance efficiently.
        """
        return Deck.objects.prefetch_related(
            Prefetch('words', queryset=ChineseWord.objects.prefetch_related(
                Prefetch('performance', queryset=WordPerformance.objects.filter(user=self.request.user))
            ))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck = self.object
        current_user = self.request.user
        words_in_deck = deck.words.all()

        if current_user.is_authenticated:
            performances = WordPerformance.objects.filter(word__in=words_in_deck, user=current_user)
            context['performances'] = performances
            deck_performance = DeckPerformance.objects.filter(deck=deck, user=current_user)
            context['deck_data'] = self.get_performance_data(deck_performance)
        else:
            context['words'] = words_in_deck

        return context

    def get_performance_data(self, deck_performances):
        data = {
            "test_dates": [],
            "percent_correct": [],
            "wrong_answers": [],
            "ids": []
        }
        for performance in deck_performances:
            data["test_dates"].append(performance.test_date.strftime('%Y-%m-%d'))
            data["percent_correct"].append(performance.percent_correct)
            data["wrong_answers"].append(performance.wrong_answers)
            data["ids"].append(performance.id)
        return data

class EditDeckView(CurrentUserMixin, UpdateView):
    model = Deck
    template_name = 'edit_deck.html'
    form_class = WordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_words'] = self.object.words.prefetch_related('deck_words')  # Optimize fetching current words
        context['word_form'] = self.get_form()  # Include the form in context
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            # Process deleted words and added words
            deleted_word_list = self.process_deleted_words(request)
            added_word_list, skipped_words_list = self.process_new_words(form.cleaned_data['new_words'])

            # Send messages to the user
            self.handle_messages(request, deleted_word_list, added_word_list, skipped_words_list)

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def process_deleted_words(self, request):
        """Handle deletion of words from the deck."""
        delete_words = request.POST.getlist('delete_word')
        if delete_words:
            deleted_word_list = ChineseWord.objects.filter(id__in=delete_words).values_list('simplified', flat=True)
            DeckWord.objects.filter(word__in=delete_words, deck=self.object).delete()
            return list(deleted_word_list)  # Convert to list to return
        return []

    def process_new_words(self, new_words):
        """Handle adding new words to the deck in bulk."""
        added_word_list = []
        skipped_words_list = []
        deck_word_instances = []  # List to hold DeckWord instances for bulk creation

        if new_words:
            word_list = re.split(r'[,\uFF0C]', new_words)  # Split by both ',' and '，'
            for simplified in map(str.strip, word_list):  # Strip whitespace
                if simplified:
                    word, created = ChineseWord.objects.get_or_create(simplified=simplified)

                    # Check if the word is already in the deck
                    if not DeckWord.objects.filter(deck=self.object, word=word).exists():
                        # Prepare a new DeckWord instance
                        deck_word_instances.append(DeckWord(deck=self.object, word=word))
                        added_word_list.append(simplified)
                    else:
                        skipped_words_list.append(simplified)

                    self.ensure_word_performance(word)

        # Bulk create all the new DeckWord instances in one go
        if deck_word_instances:
            DeckWord.objects.bulk_create(deck_word_instances)

        return added_word_list, skipped_words_list

    def ensure_word_performance(self, word):
        """Ensure that a word is added to the user's WordPerformance if it doesn't exist."""
        WordPerformance.objects.get_or_create(
            user=self.request.user,
            word=word,
            defaults={'ef_factor': 2, 'repetitions': 0, 'right': 0, 'wrong': 0}
        )

    def handle_messages(self, request, deleted_word_list, added_word_list, skipped_words_list):
        """Send messages to the user based on actions (added, deleted, skipped words)."""
        if deleted_word_list:
            messages.success(request, f"Deleted words: {', '.join(deleted_word_list)}.")
        if added_word_list:
            messages.success(request, f"New words successfully added: {', '.join(added_word_list)}.")
        if skipped_words_list:
            messages.info(request, f"These words were already in the deck: {', '.join(skipped_words_list)}.")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('frontend:edit_deck', kwargs={'pk': self.object.pk})


class DeckMixin:
    """Mixin to retrieve a deck based on the URL parameter."""

    def get_deck(self):
        deck_id = self.kwargs.get('pk')
        return get_object_or_404(Deck, id=deck_id)


class ReviewDeckMixin(DeckMixin, CurrentDateTimeMixin):
    """Mixin to filter words that are due for review."""

    def get_deck(self):
        # Retrieve the deck using the URL parameter 'pk'
        deck_id = self.kwargs.get('pk')
        return get_object_or_404(Deck, id=deck_id)

    def filter_due_words(self, deck):
        # Prefetch related performance data for the words in the deck
        words_with_performance = deck.words.prefetch_related('performance')

        due_words = []

        for word in words_with_performance:
            performance = word.performance.filter(user=self.request.user).first()
            if self.is_due_for_review(word):  # Only include if due for review
                due_words.append({
                    'word': word,
                    'performance': performance  # Will be None if no performance exists
                })

        return due_words

    def is_due_for_review(self, word):
        performance = word.performance.filter(user=self.request.user).first()
        if performance and performance.next_review_date:
            return performance.next_review_date <= timezone.now()
        return False


class ReviewDeckView(CurrentUserMixin, ReviewDeckMixin, ListView):
    model = Deck
    template_name = 'review_deck.html'
    context_object_name = 'deck'

    def get_queryset(self):
        """
        Prefetch related words and their performances for the current user using a 'double index'.
        This method retrieves Deck -> Words -> Performance efficiently.
        """
        return Deck.objects.prefetch_related(
            Prefetch('words', queryset=ChineseWord.objects.prefetch_related(
                Prefetch('performance', queryset=WordPerformance.objects.filter(user=self.request.user))
            ))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck = self.get_deck()
        context['to_test'] = self.filter_due_words(deck)
        context['deck'] = deck
        return context


class TestDeckView(CurrentUserMixin, ReviewDeckMixin, ListView):
    model = Deck
    template_name = 'test_deck.html'
    context_object_name = 'deck'

    def get_queryset(self):
        """
        Use double index to prefetch words and their performances efficiently.
        Deck -> Words -> Performance (filtered by the current user).
        """
        return Deck.objects.prefetch_related(
            Prefetch('words', queryset=ChineseWord.objects.prefetch_related(
                Prefetch('performance', queryset=WordPerformance.objects.filter(user=self.request.user))
            ))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck = self.get_deck()  # Retrieve the deck
        context['deck'] = deck  # Add deck to context

        # Use mixin method to get words due for testing
        context['to_test'] = self.filter_due_words(deck)

        return context

    def filter_due_words(self, deck):
        """
        Filter words in the deck that are due for testing, reusing the mixin method.
        """
        due_words = []
        for word in deck.words.prefetch_related('performance'):
            performance = word.performance.filter(user=self.request.user).first()
            if performance:
                due_words.append({
                    'word': word,
                    'performance': performance
                })
        return due_words

class AddDeckView(CreateView):
    model = Deck
    template_name = 'add_deck.html'
    fields = ['name']
    success_url = reverse_lazy('frontend:deck_detail')
