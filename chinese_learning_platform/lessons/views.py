from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Lesson, ReadingText, Homework, LexicalExercise
from .forms import LessonForm, ReadingTextForm, HomeworkForm, LexicalExerciseForm
from django.contrib import messages


class LessonContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_id = self.kwargs.get('lesson_id')
        context['lesson'] = get_object_or_404(Lesson, id=lesson_id)
        return context


class LessonRelatedViewMixin(LessonContextMixin):
    def form_valid(self, form):
        form.instance.lesson = self.get_context_data()['lesson']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(f'lessons:{self.model._meta.model_name}_list',
                            kwargs={'lesson_id': self.kwargs['lesson_id']})


class LessonRelatedListView(LessonContextMixin, ListView):
    def get_queryset(self):
        return self.model.objects.filter(lesson__id=self.kwargs['lesson_id'])


class LessonRelatedCreateView(LessonRelatedViewMixin, CreateView):
    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} created successfully!')
        return super().form_valid(form)


class LessonRelatedUpdateView(LessonRelatedViewMixin, UpdateView):
    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} updated successfully!')
        return super().form_valid(form)


class LessonRelatedDeleteView(LessonContextMixin, DeleteView):
    def form_valid(self, form):
        messages.success(self.request, f'{self.model._meta.verbose_name} deleted successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(f'lessons:{self.model._meta.model_name}_list',
                            kwargs={'lesson_id': self.kwargs['lesson_id']})


# Lesson views
class LessonListView(ListView):
    model = Lesson
    template_name = 'lessons/lesson_list.html'
    context_object_name = 'lessons'

from .serializers import LexicalExerciseSerializer
class LessonDetailView(DetailView):
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    context_object_name = 'lesson'
    pk_url_kwarg = 'lesson_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reading_texts'] = self.object.reading_texts.all()
        context['new_words'] = self.object.words.all()
        context['decks'] = self.object.decks.all()
        context['homeworks'] = self.object.homeworks.all()
        exercises = self.object.lexical_exercises.all()
        serialized_exercises = [LexicalExerciseSerializer(exercise).data for exercise in exercises if exercise.parent==None]
        context['lexical_exercises'] = serialized_exercises
        return context

class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/add_lesson.html'
    success_url = reverse_lazy('lessons:lesson_list')


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/edit_lesson.html'
    success_url = reverse_lazy('lessons:lesson_list')
    pk_url_kwarg = 'lesson_id'


# ReadingText views
class ReadingTextListView(LessonRelatedListView):
    model = ReadingText
    template_name = 'lessons/reading_text_list.html'
    context_object_name = 'reading_texts'


class ReadingTextCreateView(LessonRelatedCreateView):
    model = ReadingText
    form_class = ReadingTextForm
    template_name = 'lessons/add_reading_text.html'


class HomeworkListView(LessonRelatedListView):
    model = Homework
    template_name = 'lessons/homework_list.html'
    context_object_name = 'homeworks'


class HomeworkCreateView(LessonRelatedCreateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'lessons/add_homework.html'

class HomeworkUpdateView(LessonRelatedUpdateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'lessons/homework_form.html'


class HomeworkDeleteView(LessonRelatedDeleteView):
    model = Homework
    template_name = 'lessons/homework_confirm_delete.html'
    context_object_name = 'homework'


# LexicalExercise views
class LexicalExerciseListView(LessonRelatedListView):
    model = LexicalExercise
    template_name = 'lessons/lexical_exercise_list.html'
    context_object_name = 'lexical_exercises'


class LexicalExerciseCreateView(LessonRelatedCreateView):
    model = LexicalExercise
    form_class = LexicalExerciseForm
    template_name = 'lessons/add_lexical_exercise.html'


class EditLexicalExerciseView(LessonRelatedUpdateView):
    model = LexicalExercise
    form_class = LexicalExerciseForm
    template_name = 'lessons/edit_lexical_exercise.html'
    context_object_name = 'lexical_exercise'
    def get_success_url(self):
        return reverse_lazy('lessons:lexicalexercise_list', kwargs={'lesson_id': self.object.lesson.id})


# ReadingText views
class ReadingTextUpdateView(LessonRelatedUpdateView):
    model = ReadingText
    form_class = ReadingTextForm
    template_name = 'lessons/edit_reading_text.html'

class ReadingTextDeleteView(LessonRelatedDeleteView):
    model = ReadingText
    template_name = 'lessons/reading_text_confirm_delete.html'
    context_object_name = 'reading_text'

class LexicalExerciseDeleteView(LessonRelatedDeleteView):
    model = LexicalExercise
    template_name = 'lessons/lexical_exercise_confirm_delete.html'
    context_object_name = 'lexical_exercise'
