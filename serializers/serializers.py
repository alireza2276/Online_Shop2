from rest_framework import serializers
from decimal import Decimal
from store.models import Category,Order,OrderItem, Product, Comment, CartItem, Cart, Customer
from django.utils.text import slugify
from django.db import transaction



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

class OrderCustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, source='user.first_name')
    last_name = serializers.CharField(max_length=255, source='user.last_name')

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name']

class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model =Product
        fields = ['id', 'title', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product', 'quantity', 'price']



class OrderSeializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'is_paid', 'datetime_created', 'items']

class OrderForaAdminSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer = OrderCustomerSerializer()
    class Meta:
        model = Order
        fields = ['id', 'customer', 'is_paid', 'datetime_created', 'items']


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.get(id=cart_id).exist():
            return serializers.ValidationError('there is not some product in this cart')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            return serializers.ValidationError('Your cart is empty')
        return cart_id
    
    def save(self, **kwargs):
            with transaction.atomic():
        
                cart_id = self.validated_data['cart_id']
                user_id = self.context['user_id']
                customer = Customer.objects.get(user_id=user_id)

                order = Order()
                order.customer = customer
                order.save()

                cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

                order_items = list()
                for cart_item in cart_items:
                    order_item = OrderItem()
                    order_item.order = order
                    order_item.product_id = cart_item.product_id
                    order_item.price = cart_item.product.price
                    order_item.quantity = cart_item.quantity               
                    order_item.save()

                    order_items.append(order_item)
                
                OrderItem.objects.bulk_create(order_items)

                Cart.objects.get(id=cart_id).delete()

                return order


              



