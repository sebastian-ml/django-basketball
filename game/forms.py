from django import forms
from .models import Season


class SeasonSearchForm(forms.ModelForm):
    """
    Contains all available seasons.
    """
    seasons = Season.objects.values_list('year')
    seasons_tuple = [season + season for season in seasons]
    seasons_tuple.insert(0, ('Wszystkie', 'Wszystkie'))  # All seasons

    year = forms.ChoiceField(choices=seasons_tuple)

    class Meta:
        model = Season
        fields = ['year']
