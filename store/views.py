from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Product

class HomeView(TemplateView):
    template_name = 'home.html'


class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'

