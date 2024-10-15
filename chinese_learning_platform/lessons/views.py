from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Lesson, ReadingText, Homework, LexicalExercise
from .forms import LessonForm, ReadingTextForm, HomeworkForm, LexicalExerciseForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

class SuperuserRequiredMixin:
    """Mixin to ensure that only superusers can access the view."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to access this view.")
        return super().dispatch(request, *args, **kwargs)

class LessonContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson_id = self.kwargs.get('lesson_id')
        context['lesson'] = get_object_or_404(Lesson, id=lesson_id)
        return context


class LessonRelatedViewMixin(LessonContextMixin, LoginRequiredMixin):
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
        context['primary_words'] = self.object.words.all()
        context['supplementary_words'] = self.object.supplementary_words.all()
        context['understanding_words'] = self.object.words_for_understanding.all()

        context['decks'] = self.object.decks.all()
        exercises = self.object.lexical_exercises.all()
        serialized_exercises = [LexicalExerciseSerializer(exercise).data for exercise in exercises if
                                exercise.parent == None]
        context['lexical_exercises'] = serialized_exercises
        return context

class LessonCreateView(SuperuserRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/add_lesson.html'
    success_url = reverse_lazy('lessons:lesson_list')


class LessonUpdateView(SuperuserRequiredMixin, UpdateView):
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


class ReadingTextCreateView(SuperuserRequiredMixin, LessonRelatedCreateView):
    model = ReadingText
    form_class = ReadingTextForm
    template_name = 'lessons/add_reading_text.html'


class HomeworkListView(LessonRelatedListView):
    model = Homework
    template_name = 'lessons/homework_list.html'
    context_object_name = 'homeworks'

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)



class HomeworkCreateView(LoginRequiredMixin, LessonRelatedCreateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'lessons/add_homework.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class HomeworkOwnerMixin:
    """Mixin to ensure only the owner can access the homework instance."""

    def dispatch(self, request, *args, **kwargs):
        homework = self.get_object()
        if homework.user != request.user:
            return HttpResponseForbidden("You do not have permission to access this homework.")
        return super().dispatch(request, *args, **kwargs)


class HomeworkUpdateView(HomeworkOwnerMixin, LessonRelatedUpdateView):
    model = Homework
    form_class = HomeworkForm
    template_name = 'lessons/homework_form.html'


class HomeworkDeleteView(HomeworkOwnerMixin, LessonRelatedDeleteView):
    model = Homework
    template_name = 'lessons/homework_confirm_delete.html'
    context_object_name = 'homework'


# LexicalExercise views
class LexicalExerciseListView(LessonRelatedListView):
    model = LexicalExercise
    template_name = 'lessons/lexical_exercise_list.html'
    context_object_name = 'lexical_exercises'


class LexicalExerciseCreateView(SuperuserRequiredMixin, LessonRelatedCreateView):
    model = LexicalExercise
    form_class = LexicalExerciseForm
    template_name = 'lessons/add_lexical_exercise.html'


class EditLexicalExerciseView(SuperuserRequiredMixin, LessonRelatedUpdateView):
    model = LexicalExercise
    form_class = LexicalExerciseForm
    template_name = 'lessons/edit_lexical_exercise.html'
    context_object_name = 'lexical_exercise'

    def get_success_url(self):
        return reverse_lazy('lessons:lexicalexercise_list', kwargs={'lesson_id': self.object.lesson.id})


# ReadingText views
class ReadingTextUpdateView(SuperuserRequiredMixin, LessonRelatedUpdateView):
    model = ReadingText
    form_class = ReadingTextForm
    template_name = 'lessons/edit_reading_text.html'


class ReadingTextDeleteView(SuperuserRequiredMixin, LessonRelatedDeleteView):
    model = ReadingText
    template_name = 'lessons/reading_text_confirm_delete.html'
    context_object_name = 'reading_text'


class LexicalExerciseDeleteView(SuperuserRequiredMixin, LessonRelatedDeleteView):
    model = LexicalExercise
    template_name = 'lessons/lexical_exercise_confirm_delete.html'
    context_object_name = 'lexical_exercise'
