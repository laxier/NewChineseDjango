from django import forms
from .models import Lesson
from django.utils.timezone import now

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['user', 'number', 'title', 'description', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'id': 'id_date'}, format='%Y-%m-%d %H:%M:%S'),
        }

    date = forms.DateTimeField(initial=now)


