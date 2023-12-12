from django.db import models


class ActionType(models.TextChoices):
    ''' Тип действия сотрудника'''
    EXIT = 'exit'
    ENTER = 'enter'
