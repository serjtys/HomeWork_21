from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'publish_status', 'owner')
    list_filter = ('category', 'publish_status', 'owner')
    search_fields = ('name', 'description')
    list_editable = ('publish_status',)
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'price', 'image')
        }),
        ('Публикация', {
            'fields': ('publish_status', 'owner'),
            'classes': ('collapse',)
        }),
    )