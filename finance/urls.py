from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('income/', views.income, name='income'),
    path('add_revenue/', views.add_revenue, name='add_revenue'),
    path('add_cost/', views.add_cost, name='add_cost'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('download_report/', views.download_report, name='download_report'),
    path('error/', views.error_view, name='error'),
]