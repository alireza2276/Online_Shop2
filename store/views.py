from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product

class HomeView(TemplateView):
    template_name = 'home.html'


class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'



class ProductDetailView(DetailView):
    model = Product
    template_name = 'products_detail.html'
    context_object_name = 'product'
    
