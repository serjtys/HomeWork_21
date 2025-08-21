from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.shortcuts import get_object_or_404
from .models import Product
from django.urls import reverse_lazy
from .forms import ProductForm

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 6
    ordering = ['-created_at']

    def get_queryset(self):
        return Product.objects.all().order_by('-created_at')

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            print(f"Получены данные: {name}, {phone}, {message}")
        return self.render_to_response({})

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('home')