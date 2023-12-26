from rest_framework import serializers
from decimal import Decimal
from store.models import Category, Product
from django.utils.text import slugify



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title', 'num_of_products']
    title = serializers.CharField(max_length=255)
    num_of_products = serializers.SerializerMethodField()

    def get_num_of_products(self, category):
        return category.products_count


class ProductSerializers(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField()
    price_dollar = serializers.SerializerMethodField()
    category = CategorySerializer()


    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'price_dollar', 'price_after_tax', 'status', 'weight', 'ram', 'simcard', 'category']
    

    def get_price_dollar(self, product):
        return round(product.price * Decimal(0.00002), 2)
    
    def get_price_after_tax(self, product):
        return round(product.price * Decimal(0.09), 2)
    

    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product

    

