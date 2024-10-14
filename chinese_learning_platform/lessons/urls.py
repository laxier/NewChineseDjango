from django.urls import path
from .views import (
    LessonListView, LessonCreateView, LessonUpdateView, LessonDetailView,
    ReadingTextListView, ReadingTextCreateView,
    HomeworkListView, HomeworkCreateView, HomeworkUpdateView, HomeworkDeleteView,
    LexicalExerciseListView, LexicalExerciseCreateView, ReadingTextUpdateView, ReadingTextDeleteView
)

app_name = "lessons"

urlpatterns = [
    path('', LessonListView.as_view(), name='lesson_list'),
    path('add/', LessonCreateView.as_view(), name='add_lesson'),
    path('<int:lesson_id>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('<int:lesson_id>/edit/', LessonUpdateView.as_view(), name='edit_lesson'),

    path('<int:lesson_id>/reading_texts/', ReadingTextListView.as_view(), name='readingtext_list'),
    path('<int:lesson_id>/reading-text/add/', ReadingTextCreateView.as_view(), name='add_readingtext'),
    path('<int:lesson_id>/reading-text/<int:pk>/edit/', ReadingTextUpdateView.as_view(), name='edit_readingtext'),
    path('<int:lesson_id>/reading-text/<int:pk>/delete/', ReadingTextDeleteView.as_view(), name='readingtext_delete'),

    path('<int:lesson_id>/homeworks/', HomeworkListView.as_view(), name='homework_list'),
    path('<int:lesson_id>/homework/add/', HomeworkCreateView.as_view(), name='add_homework'),
    path('<int:lesson_id>/homework/<int:pk>/edit/', HomeworkUpdateView.as_view(), name='edit_homework'),
    path('<int:lesson_id>/homework/<int:pk>/delete/', HomeworkDeleteView.as_view(), name='homework_delete'),

    path('<int:lesson_id>/lexical_exercises/', LexicalExerciseListView.as_view(), name='lexical_exercise_list'),
    path('<int:lesson_id>/lexical-exercise/add/', LexicalExerciseCreateView.as_view(), name='add_lexical_exercise'),
]
