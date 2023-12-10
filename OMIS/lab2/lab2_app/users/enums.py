from django.db import models


class ActionType(models.TextChoices):
    EXIT = 'exit'
    ENTER = 'enter'
