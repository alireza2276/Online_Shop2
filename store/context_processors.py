from .views import Cart
from .models import Information, Category

def cart(request):
    return {'cart': Cart(request)}

def show_information(request):
    information = Information.objects.all().last()
    category = Category.objects.order_by('title')

    return {'information': information, 'category': category}


