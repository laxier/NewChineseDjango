from django.views.generic import UpdateView, CreateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from users.models import Deck, WordPerformance, DeckPerformance

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

    def get_queryset(self):
        return Deck.objects.prefetch_related('words')

class EditDeckView(UpdateView):
    model = Deck
    template_name = 'edit_deck.html'
    success_url = reverse_lazy('frontend:deck_detail')  

    def get_object(self, queryset=None):
        return get_object_or_404(Deck, pk=self.kwargs['pk'])

class ReviewDeckView(ListView):
    model = Deck  
    template_name = 'review_deck.html'  

class TestDeckView(ListView):
    model = Deck
    template_name = 'test_deck.html'  

class AddDeckView(CreateView):
    model = Deck
    template_name = 'add_deck.html'  
    fields = ['name']  
    success_url = reverse_lazy('frontend:deck_detail')  
