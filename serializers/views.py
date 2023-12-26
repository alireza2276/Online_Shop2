from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Product, Category
from .serializers import ProductSerializers, CategorySerializer
from rest_framework import status
from django.db.models import Count
from rest_framework.generics import ListCreateAPIView



class ProductList(ListCreateAPIView):
     serializer_class = ProductSerializers
     queryset = Product.objects.select_related('category').all()

     def get_serializer_context(self):
          return {'request': self.request}


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    
        product = get_object_or_404(Product.objects.select_related('category'), pk=pk)

        if request.method == 'GET':
            serializer = ProductSerializers(product, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'PUT':
             serializer = ProductSerializers(product, data=request.data)
             serializer.is_valid(raise_exception=True)
             serializer.save()
             return Response(serializer.data)
        
        elif request.method == 'DELETE':
             product.delete()
             return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(ListCreateAPIView):
     serializer_class = CategorySerializer
     queryset = Category.objects.prefetch_related('products').all()
     

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
         serializer = CategorySerializer(category, data=request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data)
    
    elif request.method == 'DELETE':
         category.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)

