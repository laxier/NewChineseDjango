from django.urls import path
from .views import (
    LessonListView,
    LessonCreateView,
    LessonUpdateView,
    ReadingTextCreateView,
    HomeworkCreateView,
    LexicalExerciseCreateView,
)

urlpatterns = [
    path('', LessonListView.as_view(), name='lesson_list'),
    path('add/', LessonCreateView.as_view(), name='add_lesson'),
    path('edit/<int:pk>/', LessonUpdateView.as_view(), name='edit_lesson'),
    path('lesson/<int:lesson_id>/reading-text/add/', ReadingTextCreateView.as_view(), name='add_reading_text'),
    path('lesson/<int:lesson_id>/homework/add/', HomeworkCreateView.as_view(), name='add_homework'),
    path('lesson/<int:lesson_id>/lexical-exercise/add/', LexicalExerciseCreateView.as_view(), name='add_lexical_exercise'),
]
