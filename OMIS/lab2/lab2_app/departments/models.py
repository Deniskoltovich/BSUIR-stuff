from django.db import models
from departments import abstract


class Department(abstract.IDepartment):
    name = models.CharField(max_length=64, null=False, unique=True)

    def get_name(self):
        return self.name

    def __str__(self):
        return self.get_name()
