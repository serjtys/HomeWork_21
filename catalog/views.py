from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all().order_by('-created_at')[:5]
    return render(request, 'catalog/home.html', {'products': products})

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Получены данные: {name}, {phone}, {message}")  # Для теста
    return render(request, 'catalog/contacts.html')

