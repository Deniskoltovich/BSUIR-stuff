from django.db import models

class IUserGroup(models.Model):
    class Meta:
        abstract = True

    def get_users(self):
        raise NotImplementedError

    def get_department_name(self):
        raise NotImplementedError

class IUser(models.Model):
    class Meta:
        abstract = True

    def get_password(self):
        raise NotImplementedError

    def get_fullname(self):
        raise NotImplementedError

class IEmployee(models.Model):
    class Meta:
        abstract = True

    def get_available_objects(self):
        raise NotImplementedError

    def change_password(self, new_password: str):
        raise NotImplementedError

    def get_position(self):
        raise NotImplementedError

    def get_department(self):
        raise NotImplementedError

    def get_activities(self):
        raise NotImplementedError

class IAdmin(models.Model):
    class Meta:
        abstract = True

    def get_requests(self):
        raise NotImplementedError
