from django.contrib import admin
from django.urls import path, include
from profiles.views import list_customers, update_customer, delete_customer, create_customer

urlpatterns = [
    path('', list_customers, name='list_customers'),
    path('create/', create_customer, name='create_customer'),
    path('delete/<int:id>', delete_customer, name='delete_customer'),
    path('<int:id>', update_customer, name='update_customer'),

]
