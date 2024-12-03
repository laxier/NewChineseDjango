from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Lesson, Homework
from django.contrib.auth.mixins import LoginRequiredMixin

class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "schedule/lesson_list.html"
    context_object_name = "lessons"

    def get_queryset(self):
        return Lesson.objects.filter(user=self.request.user).order_by('date')


class HomeworkListView(LoginRequiredMixin, ListView):
    model = Homework
    template_name = "schedule/homework_list.html"
    context_object_name = "homeworks"

    def get_queryset(self):
        lesson = get_object_or_404(Lesson, pk=self.kwargs['pk'], user=self.request.user)
        return Homework.objects.filter(lesson=lesson).order_by('due_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lesson'] = get_object_or_404(Lesson, pk=self.kwargs['pk'], user=self.request.user)
        return context
