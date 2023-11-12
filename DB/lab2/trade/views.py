import datetime

from django.db import connection
from django.shortcuts import render, redirect

from profiles.models import Customer
from trade.models import Bill
from trade.forms import BillCreationForm



def list_bills(request):

    qp = request.GET.get('date')
    if qp:
        bills = Bill.objects.raw(
            '''SELECT *
                FROM trade_bill
                WHERE full_price = (
                    SELECT MAX(full_price)
                    FROM trade_bill
                    WHERE strftime('%%Y-%%m-%%d', date) = %s
                );
            ''',
            [qp])
    else:
        bills = Bill.objects.raw('SELECT * FROM trade_bill;')

    context = {
        'title': 'Bills',
        'bills': bills,
    }

    return render(request, 'list_bills.html', context=context)

def update_bill(request, id):
    bill = Bill.objects.raw("SELECT * FROM trade_bill WHERE id=%s", [id])[0]
    if request.method == 'POST':
        form = BillCreationForm(request.POST, instance=bill)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE  trade_bill "
                    "SET customer_id = %s, price = %s, quantity = %s, city = %s, region = %s, country = %s "
                    "WHERE id = %s",
                    [Customer.objects.get(pk=form.cleaned_data['customer'].id).id   , form.cleaned_data['price'], form.cleaned_data['quantity'],
                     form.cleaned_data['city'], form.cleaned_data['region'], form.cleaned_data['country'], id]
                )
            return redirect('list_bills')
    else:
        form = BillCreationForm(instance=bill)

    context = {'form': form}

    return render(request, 'update_bill.html', context)

def create_bill(request):
    if request.method == 'POST':
        form = BillCreationForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO trade_bill (customer_id, price, quantity, city, region, country, date, full_price) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    [form.cleaned_data['customer'].id, form.cleaned_data['price'], form.cleaned_data['quantity'],
                     form.cleaned_data['city'], form.cleaned_data['region'], form.cleaned_data['country'], datetime.datetime.utcnow(), 0]
                )
            return redirect('list_bills')
    else:
        form = BillCreationForm

    context = {'form': form}

    return render(request, 'update_bill.html', context)


def delete_bill(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM trade_bill WHERE id=%s", [id])
    return redirect('list_bills')

