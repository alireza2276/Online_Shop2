from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from .models import Product, Category, Customer, Comment, Order, OrderItem, Contact, Information, PeriodPrice



@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'price', 'status', 'datetime_created']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(PeriodPrice)
class PeriodPriceAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_per_page = 10
    ordering = ['user']
    search_fields = ['user']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'status', 'datetime_created']
    list_editable = ['status']
    list_per_page = 10



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'datetime_created', 'is_paid']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'address', 'body', 'datetime_created']


@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone_number', 'email', 'instagram']