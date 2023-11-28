from django.db import models




class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


    def __str__(self):
        return self.title



class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='static/product_cover', blank=True)
    status = models.BooleanField(default=True)


    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title