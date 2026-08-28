# catalog/management/commands/load_products.py
import os
import json
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Загружает тестовые продукты из фикстур'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Принудительная загрузка без подтверждения',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Начинаем загрузку данных...'))

        # 1. Удаляем все существующие данные
        if not options.get('force'):
            confirm = input('⚠️  Все существующие данные будут удалены. Продолжить? (y/n): ')
            if confirm.lower() != 'y':
                self.stdout.write(self.style.WARNING('❌ Загрузка отменена'))
                return

        self.stdout.write(self.style.WARNING('🗑️  Удаляем существующие данные...'))
        Category.objects.all().delete()
        Product.objects.all().delete()

        # 2. Загружаем фикстуры
        self.stdout.write(self.style.WARNING('📥 Загружаем категории...'))
        call_command('loaddata', 'catalog/fixtures/categories.json', verbosity=0)

        self.stdout.write(self.style.WARNING('📥 Загружаем продукты...'))
        call_command('loaddata', 'catalog/fixtures/products.json', verbosity=0)

        # 3. Выводим статистику
        categories_count = Category.objects.count()
        products_count = Product.objects.count()

        self.stdout.write(self.style.SUCCESS(f'✅ Загрузка завершена!'))
        self.stdout.write(self.style.SUCCESS(f'   - Категорий: {categories_count}'))
        self.stdout.write(self.style.SUCCESS(f'   - Товаров: {products_count}'))

        # 4. Показываем примеры
        self.stdout.write(self.style.WARNING('\n📋 Примеры загруженных данных:'))
        categories = Category.objects.all()[:5]
        for cat in categories:
            self.stdout.write(f'   📂 {cat.name}: {cat.products.count()} товаров')
