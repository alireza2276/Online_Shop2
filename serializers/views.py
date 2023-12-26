from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Product, Category
from .serializers import ProductSerializers, CategorySerializer
from rest_framework import status
from django.db.models import Count


@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        queryset_products = Product.objects.select_related('category').all()
        serializer = ProductSerializers(queryset_products, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer._validated_data
        serializer.save()
        return Response('everything is ok')

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




@api_view(['GET', 'POST'])
def categpry_list(request):
     if request.method == 'GET':
        queryset_category = Category.objects.annotate(products_count=Count('products')).prefetch_related('products').all()
        serializer = CategorySerializer(queryset_category, many=True, context={'request': request})
        return Response(serializer.data)
     elif request.method == 'POST':
          serializer = CategorySerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          serializer.save()
          return Response(serializer.data, status=status.HTTP_201_CREATED)
     


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

