from django.contrib import admin
from django.urls import path, include
from products.views import list_products, update_product, delete_product, create_product, list_categories, get_products_price_changelog

urlpatterns = [
    path('', list_products, name='list_products'),
    path('create/', create_product, name='create_product'),
    path('delete/<int:id>', delete_product, name='delete_product'),
    path('changelog/<int:id>', get_products_price_changelog, name='get_products_price_changelog'),
    path('<int:id>', update_product, name='update_product'),
    path('categories/', list_categories, name='list_categories'),

]
