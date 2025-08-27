from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    paginate_by = 6
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-created_at')

        if not self.request.user.is_authenticated:
            return queryset.filter(publish_status='published')

        if not self.request.user.has_perm('catalog.can_change_publish_status'):
            return queryset.filter(publish_status='published')

        return queryset


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


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = '/users/login/'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Передаем пользователя в форму
        form.user = self.request.user
        return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Product.objects.filter(publish_status='published').order_by('-created_at')

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/users/login/'
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Передаем пользователя в форму
        form.user = self.request.user
        return form

    def get_queryset(self):
        # Только владелец может редактировать
        if self.request.user.has_perm('catalog.change_product'):
            return Product.objects.all()
        return Product.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/users/login/'
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')

