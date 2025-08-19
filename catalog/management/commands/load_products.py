from django.core.management.base import BaseCommand
from catalog.models import Product, Category
import json
import os

class Command(BaseCommand):
    help = 'Load products from JSON fixtures'

    def handle(self, *args, **options):
        # Путь к фикстурам относительно manage.py
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        categories_path = os.path.join(base_dir, 'fixtures', 'categories.json')
        products_path = os.path.join(base_dir, 'fixtures', 'products.json')

        # Очистка старых данных
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write("Old data deleted")

        # Загрузка категорий
        with open(categories_path) as f:
            categories = json.load(f)
            for cat in categories:
                Category.objects.create(
                    id=cat['pk'],
                    name=cat['fields']['name'],
                    description=cat['fields']['description']
                )
        self.stdout.write("Categories loaded")

        # Загрузка продуктов
        with open(products_path) as f:
            products = json.load(f)
            for prod in products:
                Product.objects.create(
                    id=prod['pk'],
                    name=prod['fields']['name'],
                    description=prod['fields']['description'],
                    category_id=prod['fields']['category'],
                    price=prod['fields']['price'],
                    image=prod['fields'].get('image', '')
                )
        self.stdout.write("Products loaded")