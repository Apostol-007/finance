# В файле financeapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('report/', views.generate_report, name='report'),
    path('download_report/', views.download_report, name='download_report'),
]
