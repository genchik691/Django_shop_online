from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Страница контактов
    path('contacts/', views.contacts, name='contacts'),

    # ✅ Детальная страница товара (URL вида /products/int:pk/)
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    # ✅ Добавление товара (Дополнительное задание)
    path('add-product/', views.AddProductView.as_view(), name='add_product'),
]