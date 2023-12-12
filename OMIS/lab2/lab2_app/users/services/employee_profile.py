from users.models import UserGroup, Employee
from django.contrib.auth import get_user_model

from users.abstract.services import IEmployeeProfileService


class EmployeeProfileService(IEmployeeProfileService):
    @staticmethod
    def create_profile(cleaned_data: dict):
        # получаем к какой группе относится пользователь (по названию отдела). Если такой группы нет, то создаем
        user_group, _ = UserGroup.objects.get_or_create(department_name=cleaned_data.get('department'))
        available_department = cleaned_data.pop('available_departments').first()

        employee = Employee.objects.create(user_group=user_group, **cleaned_data)
        employee.available_departments.add(available_department.id)

        username = cleaned_data.get('fullname')
        password = cleaned_data.get('password')
        EmployeeProfileService.save_profile(username, password)

    @staticmethod
    def save_profile(username: str, password:str):
        get_user_model().objects.create_user(username=username, password=password)

    @staticmethod
    def change_password(user, new_password: str):
        user.set_password(new_password)
        user.save()