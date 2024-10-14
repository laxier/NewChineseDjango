from django import forms
from chineseword.models import ChineseWord

class WordForm(forms.ModelForm):
    new_words = forms.CharField(
        max_length=500,
        required=False,
        help_text="Enter simplified words separated by commas.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите слова'})
    )

    class Meta:
        model = ChineseWord
        fields = []
