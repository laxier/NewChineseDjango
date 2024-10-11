from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

from chineseword.models import ChineseWord

User = get_user_model()

class Deck(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks_created')
    users = models.ManyToManyField(User, through='UserDeck', related_name='decks')
    words = models.ManyToManyField(ChineseWord, through='DeckWord', related_name='decks')

    def __str__(self):
        return self.name

class UserDeck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    percent = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('user', 'deck'),)

    def __str__(self):
        return f'{self.user.username} - {self.deck.name} ({self.percent}%)'

class DeckWord(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck_words')
    word = models.ForeignKey(ChineseWord, on_delete=models.CASCADE, related_name='deck_words')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('deck', 'word'),)

    def __str__(self):
        return f'{self.word} in {self.deck} added on {self.added_at}'
class WordPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(ChineseWord, on_delete=models.CASCADE, related_name='performance')
    ef_factor = models.FloatField(default=2)
    repetitions = models.IntegerField(default=0)
    right = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    next_review_date = models.DateTimeField(default=timezone.now)  # Use timezone.now directly

    _minimum_ef_factor = 1.1
    _maximum_ef_factor = 3

    class Meta:
        unique_together = (('user', 'word'),)

    @property
    def accuracy_percentage_display(self):
        if self.repetitions > 0:
            return round((self.right / (self.right + self.wrong)) * 100)
        return 0

    def calculate_interval(self, repetitions, quality):
        if repetitions == 1:
            interval = 1
        else:
            interval = round(self.ef_factor * (repetitions - 1))

        if quality < 3:
            interval = 1

        new_ef_factor = self.ef_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        self.ef_factor = max(self._minimum_ef_factor, min(new_ef_factor, self._maximum_ef_factor))
        return interval

    def correct(self):
        if self.next_review_date.replace(tzinfo=timezone.utc) >= timezone.now() and self.repetitions != 0:
            return

        if (self.right <= 1 and self.repetitions >= 3) or (self.accuracy_percentage <= 30 and self.repetitions >= 3):
            self.repetitions = 1
        else:
            self.repetitions += 1
            self.right += 1

        quality = 4
        interval = self.calculate_interval(self.repetitions, quality)
        self.edited = timezone.now()
        self.next_review_date = timezone.now() + timedelta(days=interval)

    def incorrect(self):
        if self.next_review_date.replace(tzinfo=timezone.utc) >= timezone.now() and self.repetitions != 0:
            return

        self.repetitions += 1
        self.wrong += 1
        quality = 2

        if self.accuracy_percentage >= 80:
            quality = 1

        if self.repetitions >= 7 and self.accuracy_percentage <= 86:
            self.repetitions = 1
            quality = 1

        interval = self.calculate_interval(self.repetitions, quality)
        self.edited = timezone.now()
        self.next_review_date = timezone.now() + timedelta(days=interval)

    def __str__(self):
        return f'{self.right}/{self.right + self.wrong}' if self.right or self.wrong else '0/0'

class DeckPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    percent_correct = models.IntegerField()
    test_date = models.DateTimeField(default=timezone.now)
    wrong_answers = models.TextField()

    def __str__(self):
        return f'Deck Performance: User {self.user.id}, Deck {self.deck.id}, Percent Correct {self.percent_correct}, Test Date {self.test_date}'