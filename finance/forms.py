# forms.py

from django import forms
from django.utils import timezone

class DateRangeForm(forms.Form):
    start_date = forms.DateField(label='Начальная дата', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Конечная дата', required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Если даты не указаны, выбрать последние 30 дней
        if not start_date and not end_date:
            cleaned_data['start_date'] = timezone.now().date() - timezone.timedelta(days=30)
            cleaned_data['end_date'] = timezone.now().date()

        return cleaned_data
