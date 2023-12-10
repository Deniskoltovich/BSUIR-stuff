from django.db import models
from departments.models import Department
from requests import abstract
from users.models import Employee


class Request(abstract.IRequest):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, default='Ожидание')

    def get_department(self):
        return self.department

    def get_status(self):
        return self.status

    def get_employee(self):
        return self.employee
