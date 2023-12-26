from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.products),
    path('products/<int:pk>/', views.product_detail),
    path('category/', views.categpry_list),
    path('category/<int:pk>/', views.category_detail, name='category_detail')
]