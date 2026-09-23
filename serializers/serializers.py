from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from store.models import Category, Order, OrderItem, Product, Comment, CartItem, Cart, Customer


class CategorySerializer(serializers.ModelSerializer):
    num_of_products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'num_of_products']

    def get_num_of_products(self, category):
        return category.products.count()


class ProductSerializers(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField()
    price_dollar = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'price_dollar', 'price_after_tax', 'status', 'weight', 'ram', 'simcard', 'category']

    def get_price_dollar(self, product):
        return round(Decimal(product.price) * Decimal('0.00002'), 2)

    def get_price_after_tax(self, product):
        return round(Decimal(product.price) * Decimal('1.09'), 2)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'status', 'datetime_created']
        read_only_fields = ['status', 'datetime_created']

    def create(self, validated_data):
        request = self.context['request']
        if not request.user.is_authenticated:
            raise serializers.ValidationError('Authentication is required to add a comment.')
        return Comment.objects.create(product_id=self.context['product_pk'], author=request.user, **validated_data)


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
        product = validated_data['product']
        quantity = validated_data['quantity']
        cartitem, created = CartItem.objects.get_or_create(
            cart_id=cart_id, product=product, defaults={'quantity': quantity}
        )
        if not created:
            cartitem.quantity += quantity
            cartitem.save(update_fields=['quantity'])
        return cartitem


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(read_only=True)
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
        fields = ['id', 'user', 'phone_number', 'birth_date']
        read_only_fields = ['user']


class OrderCustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name']


class OrderItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    product = OrderItemProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSeializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'is_paid', 'datetime_created', 'items']


class OrderForaAdminSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = OrderCustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'is_paid', 'datetime_created', 'items']


class OrderCreateSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError('Cart does not exist.')
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Your cart is empty.')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            customer, _ = Customer.objects.get_or_create(user_id=user_id, defaults={'phone_number': ''})
            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            OrderItem.objects.bulk_create([
                OrderItem(order=order, product=item.product, price=item.product.price, quantity=item.quantity)
                for item in cart_items
            ])
            Cart.objects.filter(id=cart_id).delete()
            return order
