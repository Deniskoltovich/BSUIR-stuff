from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, Category, PriceChangeLog
from products.forms import CategoryCreationForm, ProductCreationForm

def list_products(request):
    products = Product.objects.raw("SELECT * FROM products_product")
    print(products)
    context = {
        'title': '',
        'products': products,
    }

    return render(request, 'list_products.html', context=context)


def get_products_price_changelog(request, id):
    product = Product.objects.raw("SELECT * FROM products_product WHERE id=%s", [id])
    objs = PriceChangeLog.objects.raw("""
            SELECT * 
            FROM products_pricechangelog 
            WHERE code = %s 
            ORDER BY change_date DESC
        """, [product.code])

    context = {
        'title': 'Change log',
        'products': objs,
    }

    return render(request, 'list_price.html', context=context)

def update_product(request, id):
    product = Product.objects.raw("SELECT * FROM products_product WHERE id=%s", [id])
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, instance=product[0])
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE products_product "
                    "SET company = %s, name = %s, category_id = %s, price = %s "
                    "WHERE id = %s",
                    [form.cleaned_data['company'], form.cleaned_data['name'],
                     Category.objects.get(name=form.cleaned_data['category']).id, form.cleaned_data['price'], id]
                )
            return redirect('list_products')
    else:
        form = ProductCreationForm(instance=product[0])

    context = {'form': form}

    return render(request, 'update_product.html', context)

def create_product(request):
    if request.method == 'POST':
        form = ProductCreationForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO products_product (company, code, name, category_id, price) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    [form.cleaned_data['company'], form.cleaned_data['code'], form.cleaned_data['name'],
                     form.cleaned_data['category'], form.cleaned_data['price']]
                )
            return redirect('list_products')
    else:
        form = ProductCreationForm

    context = {'form': form}

    return render(request, 'update_product.html', context)


def delete_product(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM products_product WHERE id=%s", [id])
    return redirect('list_products')

def list_categories(request):
    ctgs = Category.objects.raw("SELECT * FROM products_category")
    context = {
        'title': 'Categories',
        'categories': ctgs,
    }
    return render(request, 'list_categories.html', context)
