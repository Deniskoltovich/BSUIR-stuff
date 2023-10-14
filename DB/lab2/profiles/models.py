from django.db import models


class Customer(models.Model):
    class Type(models.TextChoices):
        NATURAL = "Физ. лицо"
        LEGAL = "Юр. лицо"

    name = models.CharField(max_length=128, blank=False, unique=True)
    document_series = models.CharField(max_length=2, blank=False)
    document_number = models.CharField(max_length=16, blank=False)
    bank_info = models.CharField(max_length=64, blank=False)

