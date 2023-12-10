from django.shortcuts import render, redirect
from utils.common import get_current_user

from users.models import Activity

from departments.models import Department
from django.http import HttpResponse



def get_available_objects(request):
    user, is_admin = get_current_user(request)
    avail_objects = user.get_available_objects()
    context = {
        'is_admin': is_admin,
        'objects': avail_objects
    }
    return render(request, 'list_available_objects.html', context)



def enter_department(request, id):
    user, is_admin = get_current_user(request)
    department = Department.objects.get(pk=id)
    user_activity = Activity.objects.filter(user=user).first()
    if user_activity and user_activity.action == 'enter':
        return HttpResponse('Вы еще не вышли с объекта')
    Activity.objects.create(department=department, user=user, action='enter')
    return redirect('get_available_objects')


def exit_department(request):
    user, is_admin = get_current_user(request)
    user_activity = Activity.objects.filter(user=user).first()
    if not user_activity or user_activity.action == 'exit':
        return HttpResponse('Вы еще не вошли на объект')
    activity = Activity.objects.create(department=user_activity.department, user=user, action='exit')
    return redirect('get_available_objects')
