# В файле financeapp/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Income, Expense
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from .forms import DateRangeForm


def add_income(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        try:
            Income.objects.create(name=name, amount=amount, timestamp=timezone.now())
            messages.success(request, 'Доход успешно добавлен.')
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении дохода: {e}')
        return redirect('index')  # Перенаправляем на главную страницу

    return render(request, 'add_income.html')

def add_expense(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        try:
            Expense.objects.create(name=name, amount=amount, timestamp=timezone.now())
            messages.success(request, 'Расход успешно добавлен.')
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении расхода: {e}')
        return redirect('index')  # Перенаправляем на главную страницу

    return render(request, 'add_expense.html')

def index(request):
    incomes = Income.objects.all()
    expenses = Expense.objects.all()

    context = {
        'incomes': incomes,
        'expenses': expenses,
    }
    return render(request, 'index.html', context)

def generate_report(request):
    form = DateRangeForm(request.GET or None)

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        incomes = Income.objects.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
        expenses = Expense.objects.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)

    else:
        incomes = Income.objects.filter(timestamp__date__gte=timezone.now().date() - timezone.timedelta(days=30))
        expenses = Expense.objects.filter(timestamp__date__gte=timezone.now().date() - timezone.timedelta(days=30))

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'form': form,
    }

    return render(request, 'report.html', context)

def download_report(request):
    incomes = Income.objects.all()
    expenses = Expense.objects.all()

    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)

    labels = ['Доходы', 'Расходы']
    amounts = [total_income, total_expense]

    fig, ax = plt.subplots()
    ax.pie(amounts, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    img_data = f'data:image/png;base64,{img_str}'

    html = render_to_string('report.html', {
        'graph': img_data,
        'total_income': total_income,
        'total_expense': total_expense,
    })

    from weasyprint import HTML, CSS
    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 1cm }')])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response
