from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=64, blank=False, unique=True)


class Product(models.Model):
    code = models.IntegerField(unique=True, blank=False)
    name = models.CharField(max_length=64, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    price = models.DecimalField(
        max_digits=11, decimal_places=2, blank=False
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(current_price__gte=0),
                name="check_price_is_positive",
            )
        ]





