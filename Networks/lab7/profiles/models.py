from django.db import models


class Customer(models.Model):
    class Type(models.TextChoices):
        NATURAL = "Физ. лицо"
        LEGAL = "Юр. лицо"

    name = models.CharField(max_length=128, blank=False)
    document_series = models.CharField(max_length=2, blank=False)
    document_number = models.CharField(max_length=16, blank=False)
    bank_info = models.CharField(max_length=64, blank=False)
    type = models.CharField(choices=Type.choices, max_length=56, default=Type.LEGAL)

    def __str__(self):
        return f'{self.name}\nДокумент {self.document_series} {self.document_number}\nБанк: {self.bank_info}'
