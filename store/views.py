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
from .models import Product, Comment, Contact, Category, PeriodPrice
from .forms import CommentForm, AddToCartProductForm, ContactForm
from .models import OrderItem
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from .compare import Compare



def home(request):

    products = Product.objects.all()[:4]
    categories_obj = Category.objects.all()
    period_prices_obj = PeriodPrice.objects.all()


    categories = request.GET.getlist('categories')
    period_prices = request.GET.getlist('period_prices')
    sort_by = request.GET.get('sort_by')

    if sort_by:
        if sort_by == 'ASC':
            products = Product.objects.order_by('price').all()

        elif sort_by == 'DSC':
            products = Product.objects.order_by('-price').all()
    

    if len(categories):
        products = Product.objects.filter(category__title__in=categories).distinct()

    
    if len(period_prices):
        products = Product.objects.filter(period_price__title__in=period_prices).distinct()

    
    return render(request, 'home.html', context={
        'categories_obj': categories_obj,
        'categories': categories,
        'products': products,
        'sort_by': sort_by,
        'period_prices_obj': period_prices_obj,
        'period_prices': period_prices,
    })


def category(request, pk=None):
    categories = get_object_or_404(Category, id=pk)
    products =  categories.products.all()
    return render(request, 'products_list.html', {
        'categories': categories,
        'products': products,
        })



class ProductListView(ListView):
    model = Product
    paginate_by = 5
    template_name = 'products_list.html'
    context_object_name = 'products'



    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     products = Product.objects.all()
    #     categories = self.request.GET.getlist('categories')
    #     if len(categories):
    #         products = Product.objects.filter(category__title__in=categories).distinct()
        

    #     context['products'] = products
    #     context['categories_obj'] = Category.objects.all()

    #     return context

    



class ProductDetailView(DetailView):
    queryset = Product.objects.prefetch_related('comments__author')
    template_name = 'products_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        stuff = get_object_or_404(Product, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()
        context['total_likes'] = total_likes

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['liked'] = liked

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
        messages.success(self.request, _('Your comment successfully added'))

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
        
        messages.success(self.request, _('Product successfully added'))

        self.save()

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]

        messages.success(self.request, _('Product successfully removed from cart'))
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



def clear_cart(request):
    cart = Cart(request)

    if len(cart):
        cart.clear()
        messages.success(request, _('Your cart successfully removed from your cart'))

    else:
        messages.warning(request, _('Your cart is empty'))

    return redirect('products_list')

def order_create(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart)  == 0:
        messages.warning(request, _('You can not proceed, because your cart is empty!'))
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

    liked = False

    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        liked = False
    else:
        product.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('products_detail', args=[str(pk)]))

    
# contact view
class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contact.html'
    success_url = reverse_lazy('contact')


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['contact_form'] = ContactForm()
        
        return context
    

#seacrh
def search(request):
    q = request.GET.get('q')
    products = Product.objects.filter(title__icontains=q)
    return render(request, 'products_list.html', {'products': products})


# compare

def compare_detail(request):
    compare = Compare(request)
        

    return render(request, 'compare_detail.html', context={'compare': compare})



def add_to_compare(request, product_id):
    cart = Compare(request)
    product = get_object_or_404(Product, id=product_id)

    cart.add(product)

    return redirect('compare_detail')

def remove_from_compare(request, product_id):
    cart = Compare(request)
    product = get_object_or_404(Product, id=product_id)

    cart.remove(product)

    return redirect('compare_detail')