from users.abstract.services import IAccessChangingService


class AccessChangingService(IAccessChangingService):
    @staticmethod
    def remove_employee_access(employee, department):
        employee.available_departments.remove(department.id)

    @staticmethod
    def remove_group_access(user_group, department):
        for employee in user_group:
            employee.available_departments.remove(department)

    @staticmethod
    def add_employee_access(employee, department):
        employee.available_departments.add(department.id)

    @staticmethod
    def add_group_access(user_group, department):
        for employee in user_group:
            employee.available_departments.add(department.id)