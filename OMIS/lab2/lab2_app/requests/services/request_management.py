from requests.models import Request

from requests.abstract.services import IRequestManagementService


class RequestManagementService(IRequestManagementService):
    @staticmethod
    def get_requests():
        requests = Request.objects.filter(status='Ожидание')
        return requests
    @staticmethod
    def create_request(cleaned_data: dict, user):
        dep = cleaned_data.get('department')
        Request.objects.create(department=dep, employee=user)

    @staticmethod
    def change_request_status(request_id, status):
        request_ = Request.objects.get(pk=request_id)
        request_.status = status
        if status == 'Принят':
            request_.employee.available_departments.add(request_.department.id)
        request_.save()
