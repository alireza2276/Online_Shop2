from .views import Cart
from .models import Information

def cart(request):
    return {'cart': Cart(request)}

def show_information(request):
    information = Information.objects.all().last()

    return {'information': information}