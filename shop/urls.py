from django.urls import path
from . import views
from django.urls import re_path
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='products'),
    path('category/<int:id>/', views.category_products, name='category_products'),
    path('cart/', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    re_path(r'^update-cart/(?P<product_id>\d+)/(?P<change>-?\d+)/$', views.update_cart, name='update_cart'),
    path('decrease/<int:product_id>/', views.decrease_quantity, name='decrease'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('orders/', views.order_history, name='order_history'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
]