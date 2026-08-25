from django.contrib import admin
from django.urls import path, include  # ✅ Добавляем include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ✅ Подключаем URL-файл приложения catalog
    path('', include('catalog.urls')),  # Все URL заканчиваются на '/'
]

