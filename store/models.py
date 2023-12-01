from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import reverse


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


    def __str__(self):
        return self.title



class Product(models.Model):

    COLOR_CHOICES = [
        ('BLACK', 'black'),
        ('BLUE', 'blue'),
        ('WHITE', 'white'),
        ('RED', 'red'),
        ('PINK', 'pink'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='static/product_cover', blank=True)
    status = models.BooleanField(default=True)
    weight = models.IntegerField()
    color = models.CharField(max_length=255, choices=COLOR_CHOICES, default='black')



    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('products_detail', args=[self.pk])
    
    

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    

class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    image = models.ImageField(upload_to='static/user_image', blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)

    def get_absolute_url(self):
        return reverse('products_detail', args=[self.product.id])