from django.contrib import admin
from .models import Lesson, Homework


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'number', 'title', 'description')
    list_filter = ('user',)
    search_fields = ('title', 'number', 'user__username')
    ordering = ('user', 'number')


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'lesson',
        'assigned_date',
        'due_date',
        'is_completed',
        'grade',
        'is_overdue',
    )  # Поля для отображения
    list_filter = ('user', 'is_completed', 'due_date')  # Фильтры
    search_fields = ('lesson__title', 'user__username')  # Поля для поиска
    ordering = ('user', '-due_date')  # Сортировка по пользователю и дате сдачи

    def is_overdue(self, obj):
        """Отображение просроченного статуса."""
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = "Просрочено?"