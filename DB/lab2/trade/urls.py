from django.contrib import admin
from django.urls import path, include
from trade.views import create_bill, list_bills, update_bill, delete_bill



urlpatterns = [
    path('', list_bills, name='list_bills'),
    path('create/', create_bill, name='create_bill'),
    path('delete/<int:id>', delete_bill, name='delete_bill'),
    path('<int:id>', update_bill, name='update_bill'),

]
