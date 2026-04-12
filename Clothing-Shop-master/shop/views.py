from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Category, Product
from django.shortcuts import get_object_or_404

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'home.html', {'categories': categories,'products': products})


def category_products(request, id):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=selected_category)

    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
    })
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    user = User.objects.first()
    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def remove_from_cart(request, product_id):
    user = User.objects.first()
    Cart.objects.filter(user=user, product_id=product_id).delete()
    return redirect('cart')

def decrease_quantity(request, product_id):
    user = User.objects.first()
    cart_item = Cart.objects.get(user=user, product_id=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def checkout(request):
    user = User.objects.first()
    cart_items = Cart.objects.filter(user=user)

    total = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(user=user, total_price=total)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    cart_items.delete()

    return redirect('orders')

def order_history(request):
    user = User.objects.first()
    orders = Order.objects.filter(user=user)

    return render(request, 'orders.html', {'orders': orders})