from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64, blank=False, unique=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    company = models.CharField(max_length=128, default='')
    code = models.IntegerField(unique=True, blank=False)
    name = models.CharField(max_length=64, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    price = models.DecimalField(
        max_digits=11, decimal_places=2, blank=False
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte=0),
                name="check_price_is_positive",
            )
        ]
    def __str__(self):
        return self.name


class PriceChangeLog(models.Model):
    name = models.CharField(max_length=64, blank=False)
    code = models.IntegerField(unique=False, blank=False)
    company = models.CharField(max_length=128, default='')
    new_price = models.DecimalField(max_digits=11, decimal_places=2, blank=False)
    change_date = models.DateTimeField(auto_now=True)