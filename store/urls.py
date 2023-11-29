from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products_list/', views.ProductListView.as_view(), name='products_list'),
]