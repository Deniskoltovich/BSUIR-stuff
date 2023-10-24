from decimal import Decimal

from django.db import models
from profiles.models import Customer


class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(
        max_digits=11, decimal_places=2, blank=False
    )
    quantity = models.IntegerField(default=1)

    city = models.CharField(max_length=32, blank=False)
    region = models.CharField(max_length=32, default='')
    country = models.CharField(max_length=32, blank=False)
    date = models.DateField(auto_now_add=True)
    full_price = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=0),
                name="check_current_price_is_positive",
            )
        ]

    def save(self, *args, **kwargs):
        self.full_price = self.price * self.quantity
        super(Bill, self).save(*args, **kwargs)
