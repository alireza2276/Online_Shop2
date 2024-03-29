from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator
from  uuid import uuid4


class Category(models.Model):
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name_plural = _('categories')


    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(_('title'), max_length=100)


    class Meta:
        verbose_name_plural = _('colors')

    def __str__(self) -> str:
        return self.title



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_('category'))
    title = models.CharField(_('title'), max_length=255)
    description = RichTextField(_('description'))
    short_description = models.TextField(_('short_description'), blank=True)
    price = models.PositiveIntegerField(_('price'),default=0)
    discount = models.PositiveIntegerField(_('discount'),blank=True, null=True)
    image = models.ImageField(_('image'),upload_to='static/product_cover', blank=True)
    status = models.BooleanField(_('status'),default=True)
    weight = models.IntegerField(_('weight'),validators=[MinValueValidator(1)])
    color = models.ManyToManyField(Color, blank=True, related_name='color', verbose_name=_('color'))
    ram = models.CharField(_('ram'),max_length=100, blank=True)
    simcard = models.CharField(_('simcard'),max_length=100, blank=True)
    operating_system = models.CharField(_('operating_system'),max_length=100, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_likes', blank=True, verbose_name=_('likes'))


    datetime_created = models.DateTimeField(_('datetime_created'),default=timezone.now)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = ('محصولات')

    def total_likes(self):
        return self.likes.count()


    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('products_detail', args=[self.pk])
    
    
    

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('user'))
    phone_number = models.CharField(_('phone_number'),max_length=255)
    birth_date = models.DateField(_('birth_date'),null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user}"
    
    class Meta:
        verbose_name_plural = _('customer')

    

class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_('product'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments', verbose_name=_('author'))
    body = models.TextField(_('body'))
    datetime_created = models.DateTimeField(_('datetime_created'), auto_now_add=True)
    status = models.CharField(_('status'), max_length=255, choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING)

    def get_absolute_url(self):
        return reverse('products_detail', args=[self.product.id])
    
    class Meta:
        verbose_name_plural = _('comments')


class Order(models.Model):
        customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name=_('customer') )
        is_paid = models.BooleanField(_('is_paid'), default=False)

        first_name = models.CharField(_('first_name'), max_length=255)
        last_name = models.CharField(_('last_name'), max_length=255)

        phone_Number = models.CharField(_('phone_number'), max_length=15)
        address = models.CharField(_('address'), max_length=700)
        order_notes = models.CharField(_('order_notes'), max_length=700, blank=True)

        zarinpal_authority = models.CharField(max_length=255, blank=True)
        zarinpal_ref_id = models.CharField(max_length=255, blank=True)
        zarinpal_data = models.TextField(blank=True)

        datetime_created = models.DateTimeField(_('datetime_created'), auto_now_add=True)
        datetime_modified = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"{self.customer} - {self.is_paid}"
        
        def get_total_price(self):
            return sum(item.quantity * item.price for item in self.items.all())
        
        class Meta:
            verbose_name_plural = _('orders')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_item', verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'),default=1)
    price = models.PositiveIntegerField(_('price'),)

    def __str__(self):
        return f"OrderItems {self.id} : {self.product} x {self.quantity}  (price:{self.price})"
    
    class Meta:
        verbose_name_plural = _('orderitems')
    

# contact us
class Contact(models.Model):
    full_name = models.CharField(_('full_name'), max_length=255)
    email = models.EmailField(_('email'))
    address = models.CharField(_('address'), max_length=255)
    body = models.TextField(_('body'))

    datetime_created = models.DateTimeField(_('datetime_ctreated'), auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.full_name} {self.email}"
    
    class Meta:
        verbose_name_plural = _('contact')
    
#information 

class Information(models.Model):
    address = models.CharField(_('address'), max_length=255)
    phone_number = models.CharField(_('phone_number'), max_length=15)
    email = models.EmailField(_('email'), )
    instagram = models.CharField(_('instagram'), max_length=255)

    class Meta:
        verbose_name_plural = _('informations')



# for serializers

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)


    class Meta:
        verbose_name_plural = _('cart')

    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name=_('cart'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items', verbose_name=_('product'))
    quantity = models.PositiveIntegerField(_('quantity'))


    class Meta:
        verbose_name_plural = _('cartitems')

