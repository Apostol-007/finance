# finance_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_cost', views.add_cost, name='add_cost'),
    path('add_revenue', views.add_revenue, name='add_revenue'),
    path('report', views.report, name='report'),
    path('download_report', views.download_report, name='download_report'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
]

