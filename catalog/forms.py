from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category


class ProductForm(forms.ModelForm):
    # Список запрещенных слов
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта',
        'биржа', 'дешево', 'бесплатно',
        'обман', 'полиция', 'радар'
    ]

    def clean_name(self):
        name = self.cleaned_data.get('name', '').lower()
        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f'Название содержит запрещенное слово: "{word}"')
        return self.cleaned_data['name']

    def clean_description(self):
        description = self.cleaned_data.get('description', '').lower()
        for word in self.FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(f'Описание содержит запрещенное слово: "{word}"')
        return self.cleaned_data['description']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Проверка формата
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError('Поддерживаются только форматы JPEG и PNG')

            # Проверка размера (5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер файла не должен превышать 5MB')

        return image

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'publish_status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите товар подробно...',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'publish_status': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'name': 'Название товара',
            'description': 'Описание',
            'category': 'Категория',
            'price': 'Цена',
            'image': 'Изображение',
            'publish_status': 'Статус публикации'
        }

    def __init__(self, *args, **kwargs):
        # Извлекаем пользователя из kwargs
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Для обычных пользователей скрываем поле publish_status
        if not self.user or not self.user.has_perm('catalog.can_change_publish_status'):
            if 'publish_status' in self.fields:
                # Устанавливаем значение по умолчанию
                self.fields['publish_status'].initial = 'moderation'
                # Скрываем поле
                self.fields['publish_status'].widget = forms.HiddenInput()
        else:
            # Для админов убедимся, что поле видимое и имеет правильный виджет
            if 'publish_status' in self.fields:
                self.fields['publish_status'].widget = forms.Select(attrs={
                    'class': 'form-select'
                })
                # Убедимся, что choices установлены правильно
                self.fields['publish_status'].choices = Product.PUBLISH_STATUS_CHOICES