from django.urls import path

from . import views

urlpatterns = [
    path('process/', views.sandbox_payment_process, name='payment_process'),
    path('callback/', views.sandbox_payment_callback, name='payment_callback'),
]