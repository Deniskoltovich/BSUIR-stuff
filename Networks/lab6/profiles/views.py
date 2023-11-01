from profiles.forms import CustomerCreationForm
from profiles.models import Customer
from django.shortcuts import render, redirect


def list_customers(request):
    objs = Customer.objects.all()

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
    Customer.objects.get(pk=id).delete()
    return redirect('list_customers')

