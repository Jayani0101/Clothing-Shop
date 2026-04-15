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
]
