from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:id>/', views.category_products, name='category_products'),
    path('', views.product_list, name='products'),
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease/<int:product_id>/', views.decrease_quantity, name='decrease'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='orders'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
]