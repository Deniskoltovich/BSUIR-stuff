from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import AdminCreationForm, EmployeeCreationForm, ChangeGroupForm, ChangeUserForm, ChangePasswordForm
from django.contrib.auth import login, logout
from .models import Employee

from utils.common import get_current_user
from django.views import View

from .services.access_changing import AccessChangingService
from .services.employee_profile import EmployeeProfileService
from .services.registration import RegistrationService
from .services.user_management import UserManagementService


@method_decorator(login_required, name="get")
class LogoutUserView(View):
    '''Выход из системы'''

    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


class RegistrationController(View):
    '''Регистрация'''

    template_name = 'registration/register.html'

    def get(self, request):
        '''Если пользователь только зашел на страницу, просто отображаем форму'''
        form = AdminCreationForm()
        context = {'form': form, 'is_admin': True}
        return render(request, self.template_name, context)

    def post(self, request):
        '''Пользователь уже ввел данные и отправил форму'''
        form = AdminCreationForm(request.POST)

        if form.is_valid():
            form.save()
            user = RegistrationService.register(form.cleaned_data)
            login(request, user)
            return redirect(reverse('list_users'))

        context = {'form': form, 'is_admin': True}
        return render(request, self.template_name, context)


@method_decorator(login_required, name="get")
class DisplayUserController(View):
    """
    Контроллер отображения сотрудников
    """
    template_name = 'list_employees.html'

    def get(self, request, id=None):
        user, is_admin = get_current_user(request)
        # если not id, то пользователь хочет получить список сотрудников, иначе активность конкретного сотрудника
        if not id:
            if not is_admin:
                return redirect('get_available_objects')
            # получаем сотрудников для страницы просмотра сотрудников
            users = UserManagementService.get_employees()
            context = {'is_admin': is_admin, 'employees': users}
            return render(request, self.template_name, context)
        # получаем активность сотрудника для страницы активности
        employee, activities = UserManagementService.get_user_activities(id)
        context = {'employee': employee,
                   'activities': activities,
                   'is_admin': is_admin
                   }

        return render(request, 'get_activities.html', context)


@method_decorator(login_required, name="get")
@method_decorator(login_required, name="post")
class EmployeeProfileController(View):
    '''
    Контроллер управления профилем сотрудника
    '''
    template_name = 'create_employee.html'

    def get(self, request):
        '''Если пользователь только зашел на страницу, просто отображаем форму'''

        user, is_admin = get_current_user(request)
        form = EmployeeCreationForm()
        context = {'form': form, 'is_admin': is_admin}
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        '''Пользователь уже ввел данные и отправил форму'''
        user, is_admin = get_current_user(request)
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            EmployeeProfileService.create_profile(form.cleaned_data)
            return redirect(reverse('list_users'))

        context = {'form': form, 'is_admin': is_admin}
        return render(request, self.template_name, context)


@method_decorator(login_required, name="get")
@method_decorator(login_required, name="post")
class ChangePasswordController(View):
    template_name = 'change_password.html'

    def get(self, request):
        user, is_admin = get_current_user(request)
        form = ChangePasswordForm()
        context = {'form': form, 'is_admin': is_admin}
        return render(request, self.template_name, context)

    def post(self, request):
        user, is_admin = get_current_user(request)
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            EmployeeProfileService.change_password(request.user, new_password)

            return redirect(reverse('get_available_objects'))

        context = {'form': form, 'is_admin': is_admin}
        return render(request, self.template_name, context)


@method_decorator(login_required, name="get")
@method_decorator(login_required, name="post")
class ChangeUserGroupController(View):
    '''
    Контроллер изменения доступа группам
    '''
    template_name = 'change_group.html'

    def get(self, request):
        user, is_admin = get_current_user(request)
        form = ChangeGroupForm()
        context = {'form': form, 'is_admin': is_admin}
        return render(request, self.template_name, context)

    def post(self, request):
        user, is_admin = get_current_user(request)
        form = ChangeGroupForm(request.POST)

        if form.is_valid():
            # берем данные из формы
            action = form.cleaned_data.get('action')
            department_name = form.cleaned_data.get('department_name')
            user_group = Employee.objects.filter(department=department_name)
            department = form.cleaned_data.get('access_department')
            # в зависимости от действия убираем или добавляем доступ группам
            if action == 'Add':
                AccessChangingService.add_group_access(user_group, department)

            if action == 'Delete':
                AccessChangingService.remove_group_access(user_group, department)

            return redirect(reverse('list_users'))

        context = {'form': form, 'is_admin': is_admin}
        return render(request, self.template_name, context)


@method_decorator(login_required, name="get")
@method_decorator(login_required, name="post")
class ChangeAccessForUserController(View):
    '''
    Контроллер изменения доступов пользователю
    '''
    template_name = 'change_user.html'

    def get(self, request):
        user, is_admin = get_current_user(request)
        form = ChangeUserForm()
        context = {'form': form, 'is_admin': is_admin}
        return render(request, self.template_name, context)

    def post(self, request):
        user, is_admin = get_current_user(request)
        form = ChangeUserForm(request.POST)

        if form.is_valid():
            action = form.cleaned_data.get('action')
            employee = form.cleaned_data.get('user')
            dep = form.cleaned_data.get('access_department')

            if action == 'Add':
                AccessChangingService.add_employee_access(employee, dep)

            if action == 'Delete':
                AccessChangingService.remove_employee_access(employee, dep)

            return redirect(reverse('list_users'))

        context = {'form': form, 'is_admin': is_admin}
        return render(request, self.template_name, context)
