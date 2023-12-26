from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.product_detail),
    path('category/', views.CategoryList.as_view()),
    path('category/<int:pk>/', views.category_detail, name='category_detail')
]