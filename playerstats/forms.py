from django import forms
from .models import PlayerStatistics as PS


class PlayerStatisticsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label = field.help_text
            field.widget.attrs['class'] = 'form__input'

    class Meta:
        model = PS
        fields = '__all__'
