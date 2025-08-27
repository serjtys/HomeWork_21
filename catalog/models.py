from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Владелец',
        related_name='products'
    )

    PUBLISH_STATUS_CHOICES = [
        ('published', 'Опубликовано'),
        ('moderation', 'На модерации'),
        ('rejected', 'Отклонено'),
    ]

    publish_status = models.CharField(
        max_length=20,
        choices=PUBLISH_STATUS_CHOICES,
        default='moderation',
        verbose_name='Статус публикации'
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_change_publish_status", "Может изменять статус публикации"),
        ]

    def __str__(self):
        return self.name