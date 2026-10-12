# catalog/services.py
from django.core.cache import cache
from .models import Product


def get_products_by_category(category_id):
    """
    Возвращает список продуктов в категории.
    Кэширует на 10 минут по ключу category_{id}.
    """
    cache_key = f"category_{category_id}"
    products = cache.get(cache_key)

    if products is None:
        # Промах кэша — идём в БД
        products = list(
            Product.objects.filter(
                category_id=category_id,
                is_published=True
            ).select_related('category')
        )
        cache.set(cache_key, products, 60 * 10)  # 10 минут
        print(f"🔄 Cache MISS for {cache_key}")
    else:
        print(f"✅ Cache HIT for {cache_key}")

    return products

def get_all_published_products():
    """
    Возвращает все опубликованные продукты.
    Кэширует на 5 минут.
    """
    cache_key = "all_published_products"
    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.filter(is_published=True).select_related('category')
        )
        cache.set(cache_key, products, 60 * 5)  # 5 минут
        print("🔄 Cache MISS for all products")
    else:
        print("✅ Cache HIT for all products")

    return products
