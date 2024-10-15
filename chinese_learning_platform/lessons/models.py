from django.db import models
from chineseword.models import ChineseWord
from users.models import Deck
from django.contrib.auth import get_user_model

User = get_user_model()

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    decks = models.ManyToManyField(Deck, related_name='decks', blank=True)
    words = models.ManyToManyField(ChineseWord, related_name='lessons', blank=True)
    supplementary_words = models.ManyToManyField(ChineseWord, related_name='supplementary_lessons', blank=True)
    words_for_understanding = models.ManyToManyField(ChineseWord, related_name='understanding_lessons', blank=True)

    def __str__(self):
        return self.title

class LexicalExercise(models.Model):
    text = models.TextField()
    audio_file = models.FileField(upload_to='audio/')
    lesson = models.ForeignKey(Lesson, related_name='lexical_exercises', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class ReadingText(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='reading_texts', on_delete=models.CASCADE)
    text = models.TextField()
    audio_file = models.FileField(upload_to='audio/', blank=True)

class Homework(models.Model):
    lesson = models.ForeignKey('Lesson', related_name='homeworks', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='homeworks', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='homework_images/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Homework for {self.lesson} by {self.user.username}'