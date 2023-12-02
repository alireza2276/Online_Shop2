from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Comment
from .forms import CommentForm


class HomeView(TemplateView):
    template_name = 'home.html'


class ProductListView(ListView):
    model = Product
    template_name = 'products_list.html'
    context_object_name = 'products'



class ProductDetailView(DetailView):
    queryset = Product.objects.prefetch_related('comments__author')
    template_name = 'products_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        
        obj = form.save(commit=False)
       
        obj.author = self.request.user
        product_id = int(self.kwargs['product_id'])
        product = get_object_or_404(Product, id=product_id)
        obj.product = product
        messages.success(self.request, 'Your comment successfully added')

        return super().form_valid(form)
        





