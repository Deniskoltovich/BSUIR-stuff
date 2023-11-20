import requests
from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from products.forms import CategoryCreationForm, ProductCreationForm
from django.contrib.auth import authenticate, login, logout
from authentication.models import User


from api.serializers import ProductSerializer, CategorySerializer
from constants import PRODUCT_URL, CATEGORY_URL

def get_product_req(pk, serializer, url = PRODUCT_URL):
    response = requests.get(url+f'{pk}/')
    response.raise_for_status()
    jsonResponse = response.json()
    print(jsonResponse)
    customer = serializer(data=jsonResponse)
    customer.is_valid(raise_exception=True)
    return customer

def get_products_req(serializer, url = PRODUCT_URL):
    response = requests.get(url)
    response.raise_for_status()
    jsonResponse = response.json()
    print(jsonResponse)

    customers = serializer(data=jsonResponse, many=True)
    customers.is_valid(raise_exception=True)
    return customers.initial_data

def delete_product_req(pk, url = PRODUCT_URL):
    requests.delete(url + f'{pk}/')



def list_products(request):

    products = get_products_req(ProductSerializer)
    context = {
        'title': '',
        'products': products,
    }

    return render(request, 'list_products.html', context=context)

def update_product(request, id):
    if request.method == 'POST':
        form = ProductCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = ProductCreationForm()

    context = {'form': form}

    return render(request, 'update_product.html', context)

def create_product(request):
    if request.method == 'POST':
        form = ProductCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = ProductCreationForm

    context = {'form': form}

    return render(request, 'update_product.html', context)


def delete_product(request, id):
    delete_product_req(id)
    return redirect('list_products')

def list_categories(request):
    ctgs = get_products_req(CategorySerializer, CATEGORY_URL)
    context = {
        'title': 'Categories',
        'categories': ctgs,
    }
    return render(request, 'list_categories.html', context)


def delete_category(request, id):
    delete_product_req(id, CATEGORY_URL)
    return redirect('list_categories')

def create_category(request):
    if request.method == 'POST':
        form = CategoryCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = CategoryCreationForm

    context = {'form': form}

    return render(request, 'update_category.html', context)