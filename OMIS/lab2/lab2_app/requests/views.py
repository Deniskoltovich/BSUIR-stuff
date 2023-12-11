from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from utils.common import get_current_user
from .forms import RequestCreationForm
from django.views import View
from .services.request_management import RequestManagementService


@method_decorator(login_required, name="get")
@method_decorator(login_required, name="post")
class CreateRequestView(View):
    """Контроллер создания запросов на доступ """

    template_name = 'request_creation.html'

    def get(self, request):
        user, is_admin = get_current_user(request)
        form = RequestCreationForm()
        context = {'form': form, 'is_admin': is_admin}
        return render(request, self.template_name, context)

    def post(self, request):
        user, is_admin = get_current_user(request)
        form = RequestCreationForm(request.POST)

        if form.is_valid():
            RequestManagementService.create_request(form.cleaned_data, user)
            return redirect(reverse('get_available_objects'))

        context = {'form': form, 'is_admin': is_admin}
        return render(request, self.template_name, context)


@method_decorator(login_required, name="get")
class ListRequestsController(View):
    """Контроллер просмотра запросов на доступ """
    template_name = 'list_requests.html'

    def get(self, request):
        user, is_admin = get_current_user(request)

        requests = RequestManagementService.get_requests()
        context = {'requests': requests, 'is_admin': is_admin}

        return render(request, self.template_name, context)


@method_decorator(login_required, name="get")
class AcceptRequestController(View):
    """Принятия запроса на доступ"""

    def get(self, request, id):
        RequestManagementService.change_request_status(id, 'Принят')
        return redirect('list_requests')


@method_decorator(login_required, name="get")
class DeclineRequestController(View):
    """Отклонение запроса на доступ"""

    def get(self, request, id):
        RequestManagementService.change_request_status(id, 'Отклонен')
        return redirect('list_requests')
