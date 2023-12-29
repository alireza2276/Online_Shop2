from rest_framework import serializers
from decimal import Decimal
from store.models import Category, Product, Comment, CartItem, Cart, Customer
from django.utils.text import slugify



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title', 'num_of_products']
    title = serializers.CharField(max_length=255)
    num_of_products = serializers.SerializerMethodField()

    def get_num_of_products(self, category):
        return category.products.count()


class ProductSerializers(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField()
    price_dollar = serializers.SerializerMethodField()


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

    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'author']

    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id, **validated_data)


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_id = self.context['cart_pk']

        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        try:
            cartitem = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cartitem.quantity +=quantity
            cartitem.save()
        except CartItem.DoesNotExist:
            cartitem = CartItem.objects.create(cart_id=cart_id, **validated_data)
        self.instance = cartitem

            
        return cartitem


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id']

    def get_total_price(self, cart):
        return sum(item.quantity * item.product.price for item in cart.items.all())
    

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'birth_date']
        read_only_fields = ['user']