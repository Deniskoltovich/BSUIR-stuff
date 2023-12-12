from users.models import Employee

from users.abstract.services import IUserManagementService


class UserManagementService(IUserManagementService):
    @staticmethod
    def get_employees():
        # обращаемся в БД, достаем всех сотрудников
        users = Employee.objects.all()
        return users

    @staticmethod
    def get_user_activities(user_id: int):
        # обращаемся в БД, ищем сотрудника по айдишнику
        employee = Employee.objects.get(pk=user_id)
        activities = employee.get_activities()
        return employee, activities
