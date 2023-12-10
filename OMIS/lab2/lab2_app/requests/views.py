from django.shortcuts import render, redirect, reverse
from utils.common import get_current_user
from .forms import RequestCreationForm
from .models import Request


def create_request(request):
    user, is_admin = get_current_user(request)

    if request.method == 'POST':
        form = RequestCreationForm(request.POST)
        if form.is_valid():
            dep = form.cleaned_data.get('department')
            Request.objects.create(department=dep, employee=user)

            return redirect(reverse('get_available_objects'))
    else:
        form = RequestCreationForm()

    context = {'form': form,
               'is_admin': is_admin}
    return render(request, 'request_creation.html', context)

def list_requests(request):
    user, is_admin = get_current_user(request)

    requests = Request.objects.filter(status='Ожидание')
    context = {
        'requests': requests,
        'is_admin': is_admin}

    return render(request, 'list_requests.html', context)

def accept_request(request, id):
    user, is_admin = get_current_user(request)

    request_ = Request.objects.get(pk=id)
    request_.status = 'Принят'
    request_.employee.available_departments.add(request_.department.id)
    request_.save()
    return redirect('list_requests')

def decline_request(request, id):
    user, is_admin = get_current_user(request)

    request_ = Request.objects.get(pk=id)
    request_.status = 'Отклонен'
    request_.save()
    return redirect('list_requests')