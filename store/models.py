from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator



class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)


    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.title



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = RichTextField()
    short_description = models.TextField(blank=True)
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='static/product_cover', blank=True)
    status = models.BooleanField(default=True)
    weight = models.IntegerField(validators=[MinValueValidator(1)])
    color = models.ManyToManyField(Color, blank=True, related_name='color')
    ram = models.CharField(max_length=100, blank=True)
    simcard = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_likes', blank=True)


    datetime_created = models.DateTimeField(default=timezone.now)
    datetime_modified = models.DateTimeField(auto_now=True)

    def total_likes(self):
        return self.likes.count()


    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('products_detail', args=[self.pk])
    
    

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    phone_number = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}"

    

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
    body = models.TextField(_('body'))
    datetime_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)

    def get_absolute_url(self):
        return reverse('products_detail', args=[self.product.id])
    


class Order(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
        is_paid = models.BooleanField(default=False)

        first_name = models.CharField(max_length=255)
        last_name = models.CharField(max_length=255)

        phone_Number = models.CharField(max_length=15)
        address = models.CharField(max_length=700)
        order_notes = models.CharField(max_length=700, blank=True)

        zarinpal_authority = models.CharField(max_length=255, blank=True)
        zarinpal_ref_id = models.CharField(max_length=255, blank=True)
        zarinpal_data = models.TextField(blank=True)

        datetime_created = models.DateTimeField(auto_now_add=True)
        datetime_modified = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"{self.user} - {self.is_paid}"
        
        def get_total_price(self):
            return sum(item.quantity * item.price for item in self.items.all())
        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_item')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"OrderItems {self.id} : {self.product} x {self.quantity}  (price:{self.price})"
    

# contact us
class Contact(models.Model):
    full_name = models.CharField(_('full_name'), max_length=255)
    email = models.EmailField(_('email'))
    address = models.CharField(_('address'), max_length=255)
    body = models.TextField(_('body'))

    datetime_created = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.full_name} {self.email}"
    
#information 

class Information(models.Model):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    instagram = models.CharField(max_length=255)