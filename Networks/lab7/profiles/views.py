import requests

from profiles.forms import CustomerCreationForm
from profiles.models import Customer
from django.shortcuts import render, redirect
from api.serializers import CustomerlSerializer
from constants import CUSTOMER_URL

def get_customer_req(pk):
    response = requests.get(CUSTOMER_URL+f'{pk}/')
    response.raise_for_status()
    jsonResponse = response.json()
    print(jsonResponse)
    customer = CustomerlSerializer(data=jsonResponse)
    customer.is_valid(raise_exception=True)
    return customer

def get_customers_req():
    response = requests.get(CUSTOMER_URL)
    response.raise_for_status()
    jsonResponse = response.json()
    print(jsonResponse)

    customers = CustomerlSerializer(data=jsonResponse, many=True)
    customers.is_valid(raise_exception=True)
    return customers.initial_data

def delete_customer_req(pk):
    requests.delete(CUSTOMER_URL+f'{pk}/')

def list_customers(request):
    objs = get_customers_req()

    context = {
        'objs': objs
    }

    return render(request, 'list_customers.html', context=context)


def update_customer(request, id):
    obj = Customer.objects.get(pk=id)
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('list_customers')
    else:
        form = CustomerCreationForm(instance=obj)

    context = {'form': form}

    return render(request, 'update_bill.html', context)

def create_customer(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_customers')
    else:
        form = CustomerCreationForm

    context = {'form': form}

    return render(request, 'update_bill.html', context)


def delete_customer(request, id):
    delete_customer_req(id)
    return redirect('list_customers')

