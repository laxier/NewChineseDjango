from django import forms

class WordSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по иероглифу, пиньиню или переводу'})
    )

class SearchForm(forms.Form):
    search = forms.CharField(required=False, label='Поиск', widget=forms.TextInput(attrs={'class': 'form-control search-input'}))
    review_period = forms.ChoiceField(choices=[('all', 'Все слова'), ('last_week', 'За неделю'),
                                               ('last_three_days', 'За три дня'), ('last_day', 'За день')],
                                      required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    hsk_levels = forms.MultipleChoiceField(choices=[(i, f'HSK {i}') for i in range(7)],
                                           required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))


from users.models import Deck

class DeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ['name']


from django.forms import modelformset_factory
from chineseword.models import ChineseWord

class AddWordForm(forms.Form):
    simplified = forms.CharField(max_length=255, required=True)

class WordForm(forms.ModelForm):
    class Meta:
        model = ChineseWord
        fields = ['simplified']  # Add any fields you want to edit in the formset

class WordFormSet(forms.models.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instances = super().save(commit=False)
        if commit:
            for instance in instances:
                instance.save()
        return instances