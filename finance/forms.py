from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import CustomUser, Income, Expense
from django.utils import timezone

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'password1', 'password2')

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

class CustomAuthenticationForm(forms.Form):
    phone_number = forms.CharField(label='Номер телефона', max_length=100)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Дополнительные настройки формы изменения пароля можно добавить здесь

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ('user', 'amount', 'description')

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('user', 'amount', 'description')
