# Skystore

[![Django](https://img.shields.io/badge/Django-5.2.5-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-blue.svg)](https://getbootstrap.com/)

Интернет-магазин цифровых товаров

## Основные возможности

- Главная страница с товарами
- Страница контактов с формой обратной связи
- Адаптивный дизайн (работает на телефонах и ПК)
- Удобное боковое меню

## Быстрый старт

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/ваш-логин/skystore.git
   cd skystore
   ```
   
## Установка зависимостей
   ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  # ИЛИ venv\Scripts\activate  # Windows
  pip install -r requirements.txt
   ```

## Запустите сервер
   ```bash
  python manage.py runserver
   ```

## Откройте в браузере
    
    http://127.0.0.1:8000/ - главная страница

    http://127.0.0.1:8000/contacts/ - контакты

## Технологии
    
    Backend: Django 5.2
    Frontend: Bootstrap 5.3
    База данных: SQLite (для разработки)

## Структура проекта

skystore/
├── catalog/          # Основное приложение
│   ├── templates/    # Шаблоны
│   └── views.py      # Логика страниц
├── static/           # CSS/изображения
└── skystore/         # Настройки проекта