from django.contrib import admin
from .models import Lesson, LexicalExercise, ReadingText, Homework

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

@admin.register(LexicalExercise)
class LexicalExerciseAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'text', 'audio_file')
    search_fields = ('text', 'lesson__title')
    list_filter = ('lesson',)

@admin.register(ReadingText)
class ReadingTextAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'text', 'audio_file')
    search_fields = ('text', 'lesson__title')
    list_filter = ('lesson',)

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'description', 'created_at', 'image')
    search_fields = ('lesson__title', 'description')
    list_filter = ('created_at', 'lesson',)

