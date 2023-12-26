from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Product, Category
from .serializers import ProductSerializers, CategorySerializer
from rest_framework import status


@api_view()
def products(request):
    queryset_products = Product.objects.select_related('category').all()
    serializer = ProductSerializers(queryset_products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view()
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    serializer = ProductSerializers(product, context={'request': request})
    return Response(serializer.data)


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category, context={'request': request})
    return Response(serializer.data)

