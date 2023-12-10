from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import AdminCreationForm, EmployeeCreationForm, ChangeGroupForm, ChangeUserForm, ChangePasswordForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from users.models import Employee, UserGroup, Admin

from utils.common import get_current_user

def logout_user(request):
    logout(request)
    return redirect(reverse('login'))



def register(request):
    user, is_admin = get_current_user(request)

    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('fullname')
            password = form.cleaned_data.get('password')
            user = get_user_model().objects.create_user(username=username, password=password)

            user = authenticate(
                username=username,
                password=password
            )
            login(request, user)
            return redirect(reverse('list_users'))
    else:
        form = AdminCreationForm()

    context = {'form': form,
               'is_admin': is_admin}
    return render(request, 'registration/register.html', context)


def list_users(request):
    user, is_admin = get_current_user(request)
    if not is_admin:
        return redirect('get_available_objects')

    users = Employee.objects.all()
    return render(request, 'list_employees.html', {'is_admin': is_admin,'employees': users})

def create_employee(request):
    user, is_admin = get_current_user(request)

    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            user_group, _ = UserGroup.objects.get_or_create(department_name=form.cleaned_data.get('department'))
            print(form.cleaned_data.get('available_departments'))
            available_department = form.cleaned_data.pop('available_departments').first()

            employee = Employee.objects.create(user_group=user_group, **form.cleaned_data)
            employee.available_departments.add(available_department.id)

            username = form.cleaned_data.get('fullname')
            password = form.cleaned_data.get('password')

            user = get_user_model().objects.create_user(username=username, password=password)

            return redirect(reverse('list_users'))
    else:
        form = EmployeeCreationForm()

    context = {'form': form,
               'is_admin': is_admin}
    return render(request, 'create_employee.html', context)

def change_password(request):
    user, is_admin = get_current_user(request)

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            request.user.set_password('new password')
            request.user.save()
            password = form.cleaned_data.get('password')
            user, _ = get_current_user(request)
            user.change_password(password)

            return redirect(reverse('get_available_objects'))
    else:
        form = ChangePasswordForm()

    context = {'form': form,
               'is_admin': is_admin}
    return render(request, 'change_password.html', context)


def change_user_group(request):
    user, is_admin = get_current_user(request)

    if request.method == 'POST':
        form = ChangeGroupForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data.get('action')
            department_name = form.cleaned_data.get('department_name')
            employees = Employee.objects.filter(department=department_name)
            department = form.cleaned_data.get('access_department')
            if action == 'Add':
                for employee in employees:
                    employee.available_departments.add(department.id)

            if action == 'Delete':
                for employee in employees:
                    employee.available_departments.remove(department)


            return redirect(reverse('list_users'))
    else:
        form = ChangeGroupForm()

    context = {'form': form,
               'is_admin': is_admin}
    return render(request, 'change_group.html', context)


def get_user_activities(request, id):
    user, is_admin = get_current_user(request)

    employee = Employee.objects.get(pk=id)
    activities = employee.get_activities()

    return render(request, 'get_activities.html', {'employee': employee, 'activities': activities})


def change_access_for_user(request):
    user, is_admin = get_current_user(request)

    if request.method == 'POST':
        form = ChangeUserForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data.get('action')
            employee = form.cleaned_data.get('user')
            dep = form.cleaned_data.get('access_department')
            if action == 'Add':
                employee.available_departments.add(dep.id)

            if action == 'Delete':
                employee.available_departments.remove(dep)


            return redirect(reverse('list_users'))
    else:
        form = ChangeUserForm()

    context = {'form': form,
               'is_admin': is_admin}
    return render(request, 'change_user.html', context)

