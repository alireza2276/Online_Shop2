from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products_list/', views.ProductListView.as_view(), name='products_list'),
    path('products_detail/<int:pk>/', views.ProductDetailView.as_view(), name='products_detail'),
    path('comments/<int:product_id>/', views.CommentCreateView.as_view(), name='comment_create'),
    path('cart/', views.cart_detail_view, name='cart_details'),
    path('add/<int:product_id>/', views.add_to_cart_ciew, name='cart_add'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='cart_remove'),
    path('clear/', views.clear_cart, name='cart_clear'),
    path('order/create/', views.order_create, name='order_create'),
    path('likes/<int:pk>/', views.likeview, name='likes' ),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('search/', views.search, name='search'),
]