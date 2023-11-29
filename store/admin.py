from django.contrib import admin

from .models import Product, Category, Customer, Comment



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'status', 'datetime_created']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
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

    