from django import forms
from chineseword.models import ChineseWord
from users.models import Deck

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

class CreateDeckForm(forms.ModelForm):
    words = forms.ModelMultipleChoiceField(
        queryset=ChineseWord.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select select2',
            'multiple': 'multiple',
        }),
        required=False
    )

    class Meta:
        model = Deck
        fields = ['name', 'words']