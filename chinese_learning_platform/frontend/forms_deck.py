from django import forms

class WordForm(forms.ModelForm):
    new_words = forms.CharField(max_length=500, required=False, help_text="Enter simplified words separated by commas.")