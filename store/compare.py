from django.contrib import messages
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404




class Compare:
    def __init__(self, request):

        self.request = request
        self.session = request.session

        compare = self.session.get('compare')

        if not compare:
           compare = self.session['compare'] = {}

        self.compare = compare

    
    def add(self, product, quantity=1):
        product_id = str(product.id)

        if product_id not in self.compare:

            self.compare[product_id] = {'quantity': quantity}

        messages.success(self.request, 'Product added to compare')

        self.save()

    
    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.compare:

            del self.compare[product_id]

        messages.success(self.request, 'Product succesffully removed')

        self.save()

    
    def save(self):
        self.session.modified = True

    
    def __iter__(self):
        product_ids = self.compare.keys()
        products = Product.objects.filter(id__in=product_ids)

        compare = self.compare.copy()

        for product in products:
            compare[str(product.id)]['product_objs'] = product

        for item in compare.values():
            item['total_price'] = item['product_objs'].price * item['quantity']
            yield item
    









    

        




