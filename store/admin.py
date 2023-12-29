from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from jalali_date.admin import ModelAdminJalaliMixin
from .models import Product, Category, Customer, Comment, Order, OrderItem, Contact, Information, Color, Cart,CartItem
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse


class CommentTabularInline(admin.TabularInline):
    model = Comment
    fields = ['product', 'author']
    extra = 1

class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    fields = ['order', 'quantity', 'product', 'price']
    extra = 1

@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['title', 'price', 'status', 'datetime_created', 'category', 'num_of_comments']
    list_per_page = 10
    list_editable = ['price']
    ordering = ['datetime_created']
    list_filter = ['datetime_created', 'category']
    search_fields = ['title']
    inlines = [CommentTabularInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).prefetch_related('comments').annotate(comments_count=Count('comments'))

    @admin.display(ordering='comments_count')
    def num_of_comments(self, product):

        url = (
            reverse('admin:store_comment_changelist')
            + '?'
            + urlencode({
                'product__id': product.id,
            })
        )


        return format_html('<a href="{}">{}</a>', url, product.comments.count())


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'birth_date']
    list_per_page = 5
    ordering = ['user']
    


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'author', 'status', 'datetime_created']
    list_editable = ['status']
    list_per_page = 10






@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'datetime_created', 'is_paid', 'num_of_items']
    inlines = [OrderItemTabularInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).prefetch_related('items').annotate(items_count=Count('items'))
    @admin.display(ordering='items_count')
    def num_of_items(self, order):
        return order.items_count


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    autocomplete_fields = ['product']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'address', 'datetime_created']


@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone_number', 'email', 'instagram']


class CartItemInline(admin.TabularInline):
    model = CartItem
    fields = ['id', 'product', 'quantity']
    extra = 0
    min_num = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['created_at']
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']