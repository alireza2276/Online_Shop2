from rest_framework import serializers
from decimal import Decimal
from store.models import Category, Product



class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    


class ProductSerializers(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField()
    price_dollar = serializers.SerializerMethodField()
    category = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name='category_detail'
    )


    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'price_dollar', 'price_after_tax', 'category']
    

    def get_price_dollar(self, product):
        return round(product.price * Decimal(0.00002), 2)
    
    def get_price_after_tax(self, product):
        return round(product.price * Decimal(0.09), 2)
    
    

