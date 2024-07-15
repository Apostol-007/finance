# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('register/', views.register_view, name='register'),  # Убедитесь, что имя 'register' указано здесь
    # Другие URL-адреса вашего приложения
]