from django.core.cache import cache
from .models import Product, Category


def get_products_by_category(category_slug):
    cache_key = f'products_category_{category_slug}'
    cached_products = cache.get(cache_key)

    if cached_products is not None:
        return cached_products

    try:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(
            category=category,
            publish_status='published'
        ).select_related('category').order_by('-created_at')

        cache.set(cache_key, products, 60 * 60)  # Кеш на 1 час
        return products
    except Category.DoesNotExist:
        return Product.objects.none()


def get_all_products():
    cache_key = 'all_products'
    cached_products = cache.get(cache_key)

    if cached_products is not None:
        return cached_products

    products = Product.objects.filter(
        publish_status='published'
    ).select_related('category').order_by('-created_at')

    cache.set(cache_key, products, 60 * 30)  # Кеш на 30 минут
    return products


def get_product_detail(pk):
    cache_key = f'product_detail_{pk}'
    cached_product = cache.get(cache_key)

    if cached_product is not None:
        return cached_product

    try:
        product = Product.objects.select_related('category', 'owner').get(pk=pk)
        cache.set(cache_key, product, 60 * 15)  # Кеш на 15 минут
        return product
    except Product.DoesNotExist:
        return None