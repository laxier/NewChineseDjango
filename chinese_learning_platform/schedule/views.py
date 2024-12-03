from django.shortcuts import render, get_object_or_404
from .models import Lesson, Homework
from .forms import LessonForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

class LessonListView(LoginRequiredMixin, ListView):
    model = Lesson
    template_name = "schedule/lesson_list.html"
    context_object_name = "lessons"

    def get_queryset(self):
        return Lesson.objects.filter(user=self.request.user).order_by('date')

class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "schedule/lesson_form.html"
    success_url = reverse_lazy('lesson_list')

    def form_valid(self, form):
        return super().form_valid(form)


# Редактирование урока
class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "schedule/lesson_form.html"
    success_url = reverse_lazy('lesson_list')


# Удаление урока
class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = "schedule/lesson_confirm_delete.html"
    success_url = reverse_lazy('lesson_list')


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

class HomeworkCreateView(CreateView):
    model = Homework
    fields = ['user', 'lesson', 'title', 'assigned_date', 'due_date', 'is_completed', 'grade']
    template_name = "schedule/homework_form.html"
    success_url = reverse_lazy('lesson_list')

    def form_valid(self, form):
        return super().form_valid(form)


class HomeworkUpdateView(UpdateView):
    model = Homework
    fields = ['user', 'lesson', 'title', 'assigned_date', 'due_date', 'is_completed', 'grade']
    template_name = "schedule/homework_form.html"
    success_url = reverse_lazy('lesson_list')


class HomeworkDeleteView(DeleteView):
    model = Homework
    template_name = "schedule/homework_confirm_delete.html"
    success_url = reverse_lazy('lesson_list')
