from django.db import models
from chineseword.models import ChineseWord
from users.models import Deck
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models import Prefetch

User = get_user_model()


def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    decks = models.ManyToManyField(Deck, related_name='decks', blank=True)
    words = models.ManyToManyField(ChineseWord, related_name='lessons', blank=True)
    supplementary_words = models.ManyToManyField(ChineseWord, related_name='supplementary_lessons', blank=True)
    words_for_understanding = models.ManyToManyField(ChineseWord, related_name='understanding_lessons', blank=True)
    lesson_file = models.FileField(upload_to='lessons_files/', blank=True, null=True, validators=[validate_pdf])

    def __str__(self):
        return self.title


class LexicalExercise(models.Model):
    text = models.TextField()
    audio_file = models.FileField(upload_to='audio/')
    lesson = models.ForeignKey(Lesson, related_name='lexical_exercises', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    @classmethod
    def get_exercise_hierarchy(cls, lesson_id):
        """
        Получает все упражнения для урока с оптимизированной загрузкой иерархии
        """
        return (cls.objects
        .filter(lesson_id=lesson_id)
        .select_related('parent')
        .prefetch_related(
            Prefetch(
                'children',
                queryset=cls.objects.select_related('parent'),
                to_attr='_prefetched_children'
            )
        ))


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
