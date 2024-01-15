from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=255, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.code