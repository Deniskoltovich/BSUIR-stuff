from users.models import Employee

from users.abstract.services import IUserManagementService


class UserManagementService(IUserManagementService):
    @staticmethod
    def get_employees():
        users = Employee.objects.all()
        return users

    @staticmethod
    def get_user_activities(user_id: int):
        employee = Employee.objects.get(pk=user_id)
        activities = employee.get_activities()
        return employee, activities
