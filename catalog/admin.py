# catalog/admin.py
from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админке"""
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка отображения товаров в админке"""
    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_editable = ('price',)  # Можно редактировать прямо в списке
