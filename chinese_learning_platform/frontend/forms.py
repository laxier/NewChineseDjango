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
