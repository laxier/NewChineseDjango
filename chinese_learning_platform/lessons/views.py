from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Lesson, ReadingText, Homework, LexicalExercise
from .forms import LessonForm, ReadingTextForm, HomeworkForm, LexicalExerciseForm

class LessonListView(ListView):
    model = Lesson
    template_name = 'lessons/lesson_list.html'
    context_object_name = 'lessons'


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/add_lesson.html'
    success_url = reverse_lazy('lesson_list')


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/edit_lesson.html'
    success_url = reverse_lazy('lesson_list')


# Пример для ReadingTextCreateView
class ReadingTextCreateView(CreateView):
    model = ReadingText
    form_class = ReadingTextForm
    template_name = 'lessons/add_reading_text.html'

    def form_valid(self, form):
        form.instance.lesson = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])  # Устанавливаем урок
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('reading_text_list', kwargs={'lesson_id': self.kwargs['lesson_id']})


# Пример для HomeworkCreateView
class HomeworkCreateView(CreateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'lessons/add_homework.html'

    def form_valid(self, form):
        form.instance.lesson = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])  # Устанавливаем урок
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homework_list', kwargs={'lesson_id': self.kwargs['lesson_id']})


# Пример для LexicalExerciseCreateView
class LexicalExerciseCreateView(CreateView):
    model = LexicalExercise
    form_class = LexicalExerciseForm
    template_name = 'lessons/add_lexical_exercise.html'

    def form_valid(self, form):
        form.instance.lesson = get_object_or_404(Lesson, id=self.kwargs['lesson_id'])  # Устанавливаем урок
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lexical_exercise_list', kwargs={'lesson_id': self.kwargs['lesson_id']})

