from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Cost, Revenue
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from geopy.geocoders import Nominatim
from pyowm.owm import OWM
import asyncio
from asgiref.sync import sync_to_async
e = 1
async def fetch_weather_async(latitude, longitude):
    owm = OWM('83faff85b4330b1210e5fba84b2706a1')  # Замените 'your_api_key' на ваш API ключ от OpenWeatherMap
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_coords(latitude, longitude)
        weather = observation.weather
        return weather
    except Exception as e:
    # обработка ошибки
        pass

#c def index(request):
## Получаем координаты с GPS спутника
#geolocator = Nominatim(user_agent="myapp")
#location = geolocator.geocode("Алматы")
#
#if location:
#    latitude = location.latitude
#    longitude = location.longitude
#else:
#    # В случае, если координаты не удалось получить, используем значения по умолчанию
#    latitude = 52.52
#    longitude = 13.41
#
## Вызываем асинхронную функцию для получения погоды
#current_weather = await fetch_weather_async(latitude, longitude)
#
## Проверяем, что current_weather и current_weather.temperature не являются методами
#if current_weather and callable(current_weather.temperature):
#    current_weather.temperature = current_weather.temperature()  # Вызываем метод, если это так
#
## Переводим температуру из кельвинов в градусы Цельсия
#if current_weather and 'temp' in current_weather.temperature:
#    current_weather.temperature['temp'] = round(current_weather.temperature['temp'] - 273.15, 2)
##    Получаем текущее время с учётом часового пояса UTC+5
#current_time = timezone.now() + timezone.timedelta(hours=5)
#
#context = {
#    'geolocator': geolocator,
#    'current_weather': current_weather,
#    'now': current_time,
#    'session_info': request.session.session_key,
#    'wallet_status': 'У вас хороший баланс!',
#    'weather': 'Солнечно и тепло',
#    'location': location
#}
#
#return render(request, 'index.html', context)
async def index(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    if latitude and longitude:
        try:
            # Вызываем асинхронную функцию для получения погоды
            current_weather = await fetch_weather_async(latitude, longitude)

            # Проверяем, что current_weather и current_weather.temperature не являются методами
            if current_weather and callable(current_weather.temperature):
                current_weather.temperature = current_weather.temperature()  # Вызываем метод, если это так

            # Переводим температуру из кельвинов в градусы Цельсия
            if current_weather and 'temp' in current_weather.temperature:
                current_weather.temperature['temp'] = round(current_weather.temperature['temp'] - 273.15, 2)

            # Получаем текущее время с учётом часового пояса UTC+5
            current_time = timezone.now() + timezone.timedelta(hours=5)

            context = {
                'current_weather': current_weather,
                'now': current_time,
                'session_info': request.session.session_key,
                'wallet_status': 'У вас хороший баланс!',
                'weather': 'Солнечно и тепло',
                # Добавьте другие данные, которые вы хотите передать в шаблон
            }

            return render(request, 'index.html', context)
        
        except Exception as e:
            # Обработка возможных ошибок
            return HttpResponse(f"Произошла ошибка при получении погоды: {str(e)}", status=500)
    
    else:
        # Если координаты не были переданы, выполните логику для получения значения по умолчанию
        # или сообщите об ошибке
        return render(request, 'index.html', {'error_message': 'Координаты не были переданы'})

def update_location(request):
    if request.method == 'GET':
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')

        # Сохранение координат в сессии или базе данных
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude

        return HttpResponse('Координаты успешно обновлены')
    else:
        return HttpResponse(status=400)


def income(request):
    revenues = Revenue.objects.all()

    context = {
        'revenues': revenues
    }
    return render(request, 'income.html', context)


def add_revenue(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        try:
            Revenue.objects.create(name=name, amount=amount, created_at=timezone.now())
            messages.success(request, 'Доход успешно добавлен.')
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении дохода: {e}')
        return redirect('income')  # Перенаправляем на страницу с доходами

    return render(request, 'add_revenue.html')


def add_cost(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        try:
            Cost.objects.create(name=name, amount=amount, created_at=timezone.now())
            messages.success(request, 'Расход успешно добавлен.')
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении расхода: {e}')
        return redirect('index')

    return render(request, 'add_cost.html')


def generate_report(request):
    costs = Cost.objects.all()
    revenues = Revenue.objects.all()

    cost_df = pd.DataFrame([(c.name, c.amount) for c in costs], columns=['Название', 'Сумма'])
    revenue_df = pd.DataFrame([(r.name, r.amount) for r in revenues], columns=['Название', 'Сумма'])

    merged_df = pd.merge(cost_df, revenue_df, on='Название', suffixes=('_затраты', '_доходы'), how='outer')
    merged_df = merged_df.fillna(0)

    fig, ax = plt.subplots()
    ax.bar(merged_df['Название'], merged_df['Сумма_затраты'], label='Затраты')
    ax.bar(merged_df['Название'], merged_df['Сумма_доходы'], bottom=merged_df['Сумма_затраты'], label='Доходы')
    plt.legend()
    plt.xlabel('Элементы')
    plt.ylabel('Сумма')
    plt.title('Затраты и доходы')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    img_data = f'data:image/png;base64,{img_str}'

    context = {
        'graph': img_data,
        'total_costs': merged_df['Сумма_затраты'].sum(),
        'total_revenues': merged_df['Сумма_доходы'].sum(),
        'profit': merged_df['Сумма_доходы'].sum() - merged_df['Сумма_затраты'].sum()
    }

    return render(request, 'report.html', context)


def download_report(request):
    costs = Cost.objects.all()
    revenues = Revenue.objects.all()

    cost_df = pd.DataFrame([(c.name, c.amount) for c in costs], columns=['Название', 'Сумма'])
    revenue_df = pd.DataFrame([(r.name, r.amount) for r in revenues], columns=['Название', 'Сумма'])

    merged_df = pd.merge(cost_df, revenue_df, on='Название', suffixes=('_затраты', '_доходы'), how='outer')
    merged_df = merged_df.fillna(0)

    fig, ax = plt.subplots()
    ax.bar(merged_df['Название'], merged_df['Сумма_затраты'], label='Затраты')
    ax.bar(merged_df['Название'], merged_df['Сумма_доходы'], bottom=merged_df['Сумма_затраты'], label='Доходы')
    plt.legend()
    plt.xlabel('Элементы')
    plt.ylabel('Сумма')
    plt.title('Затраты и доходы')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    img_data = f'data:image/png;base64,{img_str}'

    html = render_to_string('report.html', {
        'graph': img_data,
        'total_costs': merged_df['Сумма_затраты'].sum(),
        'total_revenues': merged_df['Сумма_доходы'].sum(),
        'profit': merged_df['Сумма_доходы'].sum() - merged_df['Сумма_затраты'].sum()
    })

    pdf = HTML(string=html).write_pdf(stylesheets=[CSS(string='@page { size: A4; margin: 1cm }')])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=report.pdf'
    return response


def error_view(request):
    context = {
        'error_message': 'Произошла ошибка. Пожалуйста, повторите попытку позже.'  # Пример сообщения об ошибке
    }
    return render(request, 'error.html', context)
