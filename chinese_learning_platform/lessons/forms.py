from django import forms
from .models import Lesson, ReadingText, Homework, LexicalExercise
from chineseword.models import ChineseWord
from users.models import Deck

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'decks', 'words', 'supplementary_words', 'words_for_understanding', 'lesson_file']
        widgets = {
            'decks': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'searchable-decks'}),
            'words': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'searchable-words'}),
            'supplementary_words': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'searchable-supplementary_words'}),
            'words_for_understanding': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'searchable-words_for_understanding'}),
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
        fields = ['text', 'audio_file', 'parent']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'audio_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control', 'id': 'searchable-parent'}),  # Change to Select
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = LexicalExercise.objects.all()


