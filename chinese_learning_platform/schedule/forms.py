from django import forms
from .models import Lesson
from django.utils.timezone import now

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['user', 'number', 'title', 'description', 'date']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

    date = forms.DateTimeField(initial=now)


