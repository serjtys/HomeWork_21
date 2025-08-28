from django.urls import path
from .views import (
    HomeView, ProductDetailView, ContactsView,
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    category_products
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalog/', HomeView.as_view(), name='catalog'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='edit_product'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='delete_product'),
    path('category/<int:category_id>/', category_products, name='category_products'),
]