from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Income, Expense, CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm, PasswordChangeForm # Импортируем новую форму для аутентификации
from .forms import IncomeForm, ExpenseForm

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)  # Используем вашу кастомную форму аутентификации
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid phone number or password.'})
        else:
            return render(request, 'login.html', {'form': form, 'error_message': 'Form is not valid.'})
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    users = CustomUser.objects.all()
    return render(request, 'dashboard.html', {'users': users})

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Привязываем доход к текущему пользователю
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()

    return render(request, 'add_income.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Привязываем расход к текущему пользователю
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'add_expense.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Редирект на страницу входа после успешной регистрации
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Обновляем сессионный хеш пользователя
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')  # Редирект на текущую страницу для очистки формы
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})