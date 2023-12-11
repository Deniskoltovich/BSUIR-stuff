from django.db import models
from departments.models import Department
from users.enums import ActionType
from users.abstract import models as abstract


class UserGroup(abstract.IUserGroup):
    department_name = models.CharField(max_length=64, null=False)

    def get_users(self):
        return self.employee_set.all()

    def get_department_name(self):
        return self.department_name


class Employee(abstract.IEmployee):

    fullname = models.CharField(max_length=128, null=False)
    department = models.CharField(max_length=64, null=False)
    position = models.CharField(max_length=64, null=False)
    password = models.CharField(max_length=64, null=False)
    available_departments = models.ManyToManyField(Department)
    # TODO
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    # activities создается автоматически

    def get_available_objects(self):
        return self.available_departments.all()

    def change_password(self, new_password: str):
        self.password = new_password
        self.save()

    def get_position(self):
        return self.position

    def get_password(self):
        return self.password

    def get_fullname(self):
        return self.fullname

    def get_department(self):
        return self.department

    def get_activities(self):
        return self.activity_set.all()


class Activity(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    action = models.CharField(max_length=5, choices=ActionType)
    date = models.DateTimeField(auto_now_add=True)
    # TODO: диаграмма исправить
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']


class Admin(abstract.IAdmin):
    fullname = models.CharField(max_length=128, null=False)
    password = models.CharField(max_length=64, null=False)

    def get_password(self):
        return self.password

    def get_fullname(self):
        return self.fullname

    def get_requests(self):
        return self.request_set.all()
