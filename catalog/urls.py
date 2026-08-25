# catalog/urls.py
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),
    # Страница контактов
    path('contacts/', views.contacts, name='contacts'),
]
