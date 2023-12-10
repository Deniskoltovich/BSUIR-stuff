from django.db import models


class IDepartment(models.Model):
    class Meta:
        abstract = True
    def get_name(self):
        raise NotImplementedError
