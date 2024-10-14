from django import forms
from .models import Lesson, ReadingText, Homework, LexicalExercise

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'decks', 'words']  # Поля для создания или редактирования урока
        widgets = {
            'decks': forms.CheckboxSelectMultiple(),  # Многофункциональный виджет для выбора колод
            'words': forms.CheckboxSelectMultiple(),  # Многофункциональный виджет для выбора слов
        }

class ReadingTextForm(forms.ModelForm):
    class Meta:
        model = ReadingText
        fields = ['text', 'audio_file']  # Убираем 'lesson' из полей
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'audio_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['image', 'description']  # Убираем 'lesson' из полей
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class LexicalExerciseForm(forms.ModelForm):
    class Meta:
        model = LexicalExercise
        fields = ['text', 'audio_file']  # Убираем 'lesson' из полей
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'audio_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
