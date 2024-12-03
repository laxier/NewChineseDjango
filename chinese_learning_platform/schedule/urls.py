from django.urls import path
from .views import LessonListView, HomeworkListView

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson_list'),
    path('lessons/<int:pk>/homeworks/', HomeworkListView.as_view(), name='homework_list'),
]