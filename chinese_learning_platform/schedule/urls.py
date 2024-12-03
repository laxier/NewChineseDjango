from django.urls import path
from .views import (
    LessonListView, HomeworkListView,
    LessonCreateView, LessonUpdateView, LessonDeleteView,
    HomeworkCreateView, HomeworkUpdateView, HomeworkDeleteView, add_homework_for_lesson,
    CalendarView, LessonEventsView
)

app_name = 'schedule'

urlpatterns = [
    path('calendar/', CalendarView.as_view(), name='calendar'),
    path('calendar/events/', LessonEventsView.as_view(), name='calendar_events'),

    # Уроки
    path('lessons/', LessonListView.as_view(), name='lesson_list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('lessons/<int:pk>/edit/', LessonUpdateView.as_view(), name='lesson_update'),
    path('homework/add-for-lesson/<int:lesson_id>/', add_homework_for_lesson, name='homework_create_from_lesson'),
    path('lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_delete'),

    # Домашние задания
    path('lessons/<int:pk>/homeworks/', HomeworkListView.as_view(), name='homework_list'),
    path('homeworks/create/', HomeworkCreateView.as_view(), name='homework_create'),
    path('homeworks/<int:pk>/edit/', HomeworkUpdateView.as_view(), name='homework_update'),
    path('homeworks/<int:pk>/delete/', HomeworkDeleteView.as_view(), name='homework_delete'),
]
