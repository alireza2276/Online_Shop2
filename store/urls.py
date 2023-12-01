from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products_list/', views.ProductListView.as_view(), name='products_list'),
    path('products_detail/<int:pk>/', views.ProductDetailView.as_view(), name='products_detail'),
    path('comments/<int:product_id>/', views.CommentCreateView.as_view(), name='comment_create'),
]