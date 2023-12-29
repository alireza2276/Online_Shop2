from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from store.models import Product, Category, Comment, Cart,CartItem, Customer
from .serializers import ProductSerializers, CategorySerializer, CommentSerializer, CartSerializer, CartItemSerializer,AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer
from rest_framework import status
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from .paginations import DefaultPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsAdminUserOrReadOnly


class ProductViewSet(ModelViewSet):
     serializer_class = ProductSerializers
     queryset = Product.objects.select_related('category').all()
     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
     filterset_fields = ['category_id', 'ram', 'price']
     ordering_fields = ['title', 'datetime_created']
     search_fields = ['title', 'category__title']
     pagination_class = DefaultPagination

     def get_serializer_context(self):
          return {'request': self.request}
     
     def destroy(self, request, pk):
          product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
          product.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(ModelViewSet):
     serializer_class = CategorySerializer
     queryset = Category.objects.prefetch_related('products')
     permission_classes = [IsAdminUserOrReadOnly]

     def delete(self, request, pk,*args, **kwargs ):
          category = get_object_or_404(Category.objects.prefetch_related('products'), pk=pk)
         
          category.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
     serializer_class = CommentSerializer
     queryset = Comment.objects.select_related('comments').all()

     def get_queryset(self):
          product_pk = self.kwargs['product_pk']
          return Comment.objects.filter(product_id=product_pk).all()
     
     def get_serializer_context(self):
          return {'product_pk': self.kwargs['product_pk']}
     

class CartItemViewSet(ModelViewSet):
     http_method_names = ['get', 'post', 'patch', 'delete']
     serializer_class = CartItemSerializer

     def get_queryset(self):
          cart_pk = self.kwargs['cart_pk']
          return CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()
     
     def get_serializer_class(self):
          if self.request.method == 'POST':
               return AddCartItemSerializer
          
          elif self.request.method == 'PATCH':
               return UpdateCartItemSerializer
          return CartItemSerializer
          

     def get_serializer_context(self):
          return {'cart_pk': self.kwargs['cart_pk']}
     
class CartViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
     serializer_class = CartSerializer
     queryset = Cart.objects.prefetch_related('items__product').all()
     lookup_value_regex = '[0-9a-fA-F]{8}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{12}'


class CustomerViewSet(ModelViewSet):
     serializer_class = CustomerSerializer
     queryset = Customer.objects.all()
     permission_classes = [IsAdminUser]

     @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
     def me(self, request):
          user_id = request.user.id
          customer = Customer.objects.get(user_id=user_id)

          if request.method == 'GET':

               serializer = CustomerSerializer(customer)
               return Response(serializer.data)
          elif request.method == 'PUT':
               serializer = CustomerSerializer(customer, data=request.data)
               serializer.is_valid(raise_exception=True)
               serializer.save()
               return Response(serializer.data)
