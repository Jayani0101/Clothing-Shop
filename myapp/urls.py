from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),   
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('all-products/', views.all_products, name='all_products'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites, name='favorites'),
    path('latest/', views.latest_products_view, name='latest_products'),
]
