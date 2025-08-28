from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import Product, Category
from .forms import ProductForm
from .services import get_all_products, get_product_detail, get_products_by_category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    paginate_by = 6
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category').order_by('-created_at')

        # Для неавторизованных - только опубликованное
        if not self.request.user.is_authenticated:
            return queryset.filter(publish_status='published')

        # Для обычных пользователей - опубликованное + свои товары
        if not self.request.user.has_perm('catalog.can_change_publish_status'):
            return queryset.filter(
                models.Q(publish_status='published') |
                models.Q(owner=self.request.user)
            )

        # Для админов/модеров - ВСЕ товары
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')

        # Кешируем только данные продукта
        if cache.get('cache_enabled'):
            product = get_product_detail(pk)
            if product:
                return product

        return get_object_or_404(Product.objects.select_related('category', 'owner'), pk=pk)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            print(f"Получены данные: {name}, {phone}, {message}")
        return self.render_to_response({})


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = '/users/login/'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        """Передаем пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user

        # Для обычных пользователей ставим статус "на модерации"
        if not self.request.user.has_perm('catalog.can_change_publish_status'):
            form.instance.publish_status = 'moderation'

        cache.delete('all_products')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/users/login/'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_form_kwargs(self):
        """Передаем пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        # Для админов - все товары
        if self.request.user.has_perm('catalog.can_change_publish_status'):
            return Product.objects.all()
        # Для обычных пользователей - только свои товары
        return Product.objects.filter(owner=self.request.user)

    def form_valid(self, form):
        # Инвалидируем кеши при обновлении продукта
        cache.delete('all_products')
        cache.delete(f'product_detail_{self.object.pk}')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/users/login/'
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        # Инвалидируем кеши при удалении продукта
        product_id = self.get_object().pk
        cache.delete('all_products')
        cache.delete(f'product_detail_{product_id}')
        return super().delete(request, *args, **kwargs)

def category_products(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(
            category=category,
            publish_status='published'
        ).select_related('category').order_by('-created_at')

        context = {
            'products': products,
            'category_name': category.name,
            'categories': Category.objects.all()
        }
        return render(request, 'catalog/category_products.html', context)
    except Category.DoesNotExist:
        return render(request, 'catalog/category_products.html', {
            'products': [],
            'categories': Category.objects.all()
        })