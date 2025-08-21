from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import ProductForm
from django.core.paginator import Paginator


def home(request):
    products_list = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products_list, 6)  # 6 товаров на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/home.html', {'page_obj': page_obj})

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Получены данные: {name}, {phone}, {message}")  # Для теста
    return render(request, 'catalog/contacts.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'catalog/add_product.html', {'form': form})