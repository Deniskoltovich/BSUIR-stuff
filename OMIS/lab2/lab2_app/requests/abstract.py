from django.db import models


class IRequest(models.Model):
    class Meta:
        abstract = True
    def get_employee(self):
        raise NotImplementedError

    def get_department(self):
        raise NotImplementedError

    def get_status(self):
        raise NotImplementedError

    def set_status(self):
        raise NotImplementedError
