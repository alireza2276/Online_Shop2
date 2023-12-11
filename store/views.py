from typing import Any
from django.forms.models import BaseModelForm
from .forms import OrderForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Product, Comment
from .forms import CommentForm, AddToCartProductForm
from .models import OrderItem
from django.urls import reverse


class HomeView(TemplateView):
    template_name = 'home.html'


class ProductListView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'products_list.html'
    context_object_name = 'products'



class ProductDetailView(DetailView):
    queryset = Product.objects.prefetch_related('comments__author')
    template_name = 'products_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(Product, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context['total_likes'] = total_likes
        context['comment_form'] = CommentForm()
        context['add_to_cart_form'] = AddToCartProductForm()
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
        

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    
    def add(self, product, quantity=1, replace_current_quantity=False):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}
        if replace_current_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        messages.success(self.request, 'Product successfully added')

        self.save()

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

        messages.success(self.request, 'Product successfully removed from cart')
        self.save()

    
    def save(self):
        self.session.modified = True

    
    def __iter__(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product_obj'] = product

        for item in cart.values():
            item['total_price'] = item['product_obj'].price * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def clear(self):
        del self.session['cart']
        self.save()

    def get_total_price(self):
        product_ids = self.cart.keys()

        return sum(item['product_obj'].price * item['quantity'] for item in self.cart.values())
    

def cart_detail_view(request):
    cart = Cart(request)

    for item in cart:
        item['product_update_quantity_form'] = AddToCartProductForm(initial={
            'quantity': item['quantity'],
            'inplace': True,
        })

    return render(request, 'cart_details.html', {'cart': cart})


@login_required
def add_to_cart_ciew(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddToCartProductForm(request.POST)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        quantity = cleaned_data['quantity']
        cart.add(product, quantity, replace_current_quantity=cleaned_data['inplace'])

    return redirect('cart_details')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect('cart_details')


@require_POST
def clear_cart(request):
    cart = Cart(request)

    if len(cart):
        cart.clear()
        messages.success(request, 'Your cart successfully removed from your cart')

    else:
        messages.warning(request, 'Your cart is empty')

    return redirect('products_list')

@login_required
def order_create(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart)  == 0:
        messages.warning(request, 'You can not proceed, because your cart is empty!')
        return redirect('products_list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()


            for item in cart:
                product = item['product_obj']
                OrderItem.objects.create(
                    order = order_obj,
                    product = product,
                    quantity = item['quantity'],
                    price = product.price,
                )
            
            cart.clear()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()

            request.session['order_id'] = order_obj.id
            return redirect('payment_process')
             
    return render(request, 'order_create.html', context={
        'form': order_form
    })

# Like Product
@login_required
def likeview(request, pk):
    product = get_object_or_404(Product, id=request.POST.get('product_id'))
    product.likes.add(request.user)
    return HttpResponseRedirect(reverse('products_detail', args=[str(pk)]))

    









