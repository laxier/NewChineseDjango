from django import forms
from .models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['user', 'number', 'title', 'description', 'date']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

