from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

class Lesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons', verbose_name="Пользователь")
    number = models.PositiveIntegerField("Номер урока")
    title = models.CharField("Название урока", max_length=255)
    description = models.TextField("Описание", blank=True, null=True)
    date = models.DateField("Дата проведения", default=now)

    def __str__(self):
        return f"Урок {self.number}: {self.title} (Дата: {self.date}, Пользователь: {self.user.username})"


class Homework(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='schedule_homeworks',
        verbose_name="Пользователь"
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='homeworks',
        verbose_name="Урок"
    )
    title = models.CharField("Задание", max_length=255)
    assigned_date = models.DateField("Дата задания", default=now)
    due_date = models.DateField("Дата сдачи")
    is_completed = models.BooleanField("Выполнено", default=False)
    grade = models.PositiveIntegerField("Оценка", blank=True, null=True)

    @property
    def is_overdue(self):
        return not self.is_completed and now().date() > self.due_date

    def __str__(self):
        return f"Домашнее задание {self.lesson.title} для {self.user.username}"
