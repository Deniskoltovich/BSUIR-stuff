import datetime
from decimal import Decimal

from django.db import connection
from django.shortcuts import render, redirect

from profiles.models import Customer
from trade.models import Bill
from trade.forms import BillCreationForm
from constants import BILL_URL
import requests
from api.serializers import BillSerializer

def get_bill_req(pk):
    response = requests.get(BILL_URL+f'{pk}/')
    response.raise_for_status()
    jsonResponse = response.json()
    bill = BillSerializer(data=jsonResponse)
    bill.is_valid(raise_exception=True)
    return bill.initial_data

def get_bills_req():
    response = requests.get(BILL_URL)
    response.raise_for_status()
    jsonResponse = response.json()
    bills = BillSerializer(data=jsonResponse, many=True)
    bills.is_valid(raise_exception=True)
    return bills.initial_data

def delete_bill_req(pk):
    requests.delete(BILL_URL+f'{pk}/')

def list_bills(request):
    print(request.user)
    context = {
        'title': 'Bills',
        'bills': get_bills_req(),
    }

    return render(request, 'list_bills.html', context=context)

def update_bill(request, id):
    bill = get_bill_req(id)
    if request.method == 'POST':
        form = BillCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_bills')
    else:
        form = BillCreationForm()

    context = {'form': form}

    return render(request, 'update_bill.html', context)

def create_bill(request):
    if request.method == 'POST':
        form = BillCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_bills')
    else:
        form = BillCreationForm

    context = {'form': form}

    return render(request, 'update_bill.html', context)


def delete_bill(request, id):
    delete_bill_req(id)
    return redirect('list_bills')

