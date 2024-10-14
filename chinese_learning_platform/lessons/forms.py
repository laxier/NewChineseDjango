from django import forms
from .models import Lesson, ReadingText, Homework, LexicalExercise
from chineseword.models import ChineseWord
from users.models import Deck

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'decks', 'words']
        widgets = {
            'decks': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'searchable-decks'}),
            'words': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'searchable-words'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['decks'].queryset = Deck.objects.all()
        self.fields['words'].queryset = ChineseWord.objects.all()

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
