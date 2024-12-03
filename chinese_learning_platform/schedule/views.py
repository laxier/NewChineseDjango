from django.shortcuts import render, get_object_or_404
from .models import Lesson, Homework
from .forms import LessonForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.utils.timezone import now


class CalendarView(TemplateView):
    template_name = "schedule/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Можно добавить дополнительные данные для шаблона, если нужно
        return context


class LessonEventsView(TemplateView):
    """Provides JSON data for calendar events, including lessons and homeworks."""

    def get(self, request, *args, **kwargs):
        # Fetch all lessons
        lessons = Lesson.objects.all()
        lesson_events = [
            {
                "title": f"{lesson.title} 第{lesson.number}课",
                "start": lesson.date.strftime("%Y-%m-%dT%H:%M:%S"),
                "url": f"/schedule/lessons/{lesson.pk}/edit/",
                "color": "#007bff",  # Blue color for lessons
            }
            for lesson in lessons
        ]

        # Fetch all homeworks
        homeworks = Homework.objects.all()
        homework_events = [
            {
                "title": f"ДЗ: {homework.title}",
                "start": homework.due_date.strftime("%Y-%m-%d"),
                "url": f"/schedule/homeworks/{homework.pk}/edit/",
                "color": (
                    "#28a745"  # Green for completed
                    if homework.is_completed
                    else "#dc3545"  # Red for overdue
                    if now().date() > homework.due_date
                    else "#ffc107"  # Yellow for pending
                ),
            }
            for homework in homeworks
        ]

        # Combine both events
        events = lesson_events + homework_events
        return JsonResponse(events, safe=False)


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
    success_url = reverse_lazy('schedule:calendar')

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['user'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        print("Form is being saved for user:", self.request.user)
        return super().form_valid(form)


# Редактирование урока
class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "schedule/lesson_form.html"
    success_url = reverse_lazy('schedule:calendar')


# views.py
from django.shortcuts import redirect, get_object_or_404
from .models import Lesson


def add_homework_for_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    request.session['current_lesson_id'] = lesson_id  # Сохраняем lesson_id в сессию
    return redirect('schedule:homework_create')  # Перенаправляем на форму создания домашнего задания


# Удаление урока
class LessonDeleteView(DeleteView):
    model = Lesson
    template_name = "schedule/lesson_confirm_delete.html"
    success_url = reverse_lazy('schedule:calendar')


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
    success_url = reverse_lazy('schedule:calendar')

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['user'] = self.request.user
        lesson_id = self.request.session.get('current_lesson_id')
        if lesson_id:
            lesson = get_object_or_404(Lesson, pk=lesson_id)
            initial['lesson'] = lesson
            if lesson.date:
                initial['due_date'] = lesson.date.date()
        return initial


def form_valid(self, form):
    form.instance.user = self.request.user
    if 'current_lesson_id' in self.request.session:
        del self.request.session['current_lesson_id']
    return super().form_valid(form)


class HomeworkUpdateView(UpdateView):
    model = Homework
    fields = ['user', 'lesson', 'title', 'assigned_date', 'due_date', 'is_completed', 'grade']
    template_name = "schedule/homework_form.html"
    success_url = reverse_lazy('schedule:calendar')


class HomeworkDeleteView(DeleteView):
    model = Homework
    template_name = "schedule/homework_confirm_delete.html"
    success_url = reverse_lazy('schedule:calendar')
