from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.common import get_current_user

from django.views import View

from departments.models import Department
from django.http import HttpResponse

from departments.services.user_actions import UserActionsService, EnterError, ExitError


@method_decorator(login_required, name="get")
class AvailableObjectsController(View):
    '''Контроллер просмотра доступных объектов'''

    def get(self, request):
        user, is_admin = get_current_user(request)
        avail_objects = user.get_available_objects()
        context = {
            'is_admin': is_admin,
            'objects': avail_objects
        }
        return render(request, 'list_available_objects.html', context)


@method_decorator(login_required, name="get")
class EnterDepartmentController(View):
    '''Контроллер входа на объект'''

    def get(self, request, id):
        user, is_admin = get_current_user(request)
        department = Department.objects.get(pk=id)
        try:
            UserActionsService.do_enter(user, department)
        except EnterError:
            return HttpResponse('Вы еще не вышли с объекта')

        return redirect('get_available_objects')


@method_decorator(login_required, name="get")
class ExitDepartmentController(View):
    '''Контроллер выхода с объекта'''

    def get(self, request):
        user, is_admin = get_current_user(request)
        try:
            UserActionsService.do_exit(user)
        except ExitError:
            return HttpResponse('Вы еще не вошли на объект')

        return redirect('get_available_objects')
