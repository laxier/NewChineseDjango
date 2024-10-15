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
from .serializers import WrongAnswerSerializer
from django.http import JsonResponse
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
        return Deck.objects.select_related('creator').prefetch_related(
            Prefetch(
                'words',
                queryset=self.get_words_queryset(),
                to_attr='prefetched_words'
            )
        )

    def get_words_queryset(self):
        words_queryset = ChineseWord.objects.all()
        if self.request.user.is_authenticated:
            return words_queryset.prefetch_related(
                Prefetch(
                    'performance',
                    queryset=WordPerformance.objects.filter(user=self.request.user),
                    to_attr='user_performance'
                )
            )
        return words_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck = self.object
        current_user = self.request.user

        if current_user.is_authenticated:
            context['performances'] = self.get_user_performances(deck.prefetched_words)
            context['deck_data'] = self.get_performance_data(
                DeckPerformance.objects.filter(deck=deck, user=current_user).prefetch_related('wrong_answers')
            )
            context["in_user_cards"] = deck in current_user.decks.all()
        else:
            context['words'] = deck.prefetched_words
            context["in_user_cards"] = False

        return context

    def get_user_performances(self, words):
        # Use a dictionary for faster access
        performance_dict = {word.id: word.user_performance[0] if word.user_performance else None for word in words}
        return [performance_dict[word.id] for word in words]

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

            # Serialize wrong answers only once since they are prefetched
            wrong_word_details = performance.wrong_answers.all()
            serializer = WrongAnswerSerializer(wrong_word_details, many=True)
            data["wrong_answers"].append(serializer.data)

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
        # Prefetch words and their performance data
        words_with_performance = deck.words.prefetch_related(
            Prefetch('performance', queryset=WordPerformance.objects.filter(user=self.request.user))
        )
        performances = WordPerformance.objects.filter(user=self.request.user,
                                                      word__in=words_with_performance).select_related('word')
        performance_map = {performance.word_id: performance for performance in performances}

        due_words = []

        for word in words_with_performance:
            performance = performance_map.get(word.id)  # This will be None if no performance exists
            if self.is_due_for_review(word, performance):
                due_words.append({
                    'word': word,
                    'performance': performance
                })

        return due_words

    def is_due_for_review(self, word, performance):
        if performance:
            return performance.next_review_date <= timezone.now()
        return False


class ReviewDeckView(CurrentUserMixin, ReviewDeckMixin, ListView):
    model = Deck
    template_name = 'review_deck.html'
    context_object_name = 'deck'

    def get_queryset(self):
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
        return Deck.objects.prefetch_related(
            Prefetch('words', queryset=ChineseWord.objects.prefetch_related(
                Prefetch('performance', queryset=WordPerformance.objects.filter(user=self.request.user))
            ))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deck = self.get_deck()
        context['deck'] = deck
        context['to_test'] = self.filter_due_words(deck)
        return context

    def get_deck(self):
        deck_id = self.kwargs.get('pk')
        return get_object_or_404(Deck, id=deck_id)

    def is_due_for_review(self, word, performance):
        return True

from .forms_deck import CreateDeckForm
class CreateDeckView(CreateView):
    form_class = CreateDeckForm
    template_name = 'create_deck.html'
    def get_success_url(self):
        return reverse_lazy('frontend:user_decks', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        self.object.users.add(self.request.user)
        return response


class AddDeckView(CreateView):
    model = Deck
    template_name = 'add_deck.html'
    fields = ['name']
    success_url = reverse_lazy('frontend:deck_detail')


from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class DeleteDeckView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Deck

    def get_success_url(self):
        return reverse_lazy('frontend:user_decks', kwargs={'username': self.request.user.username})

    def test_func(self):
        deck = self.get_object()
        return self.request.user == deck.creator

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            raise
    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
