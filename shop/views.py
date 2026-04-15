from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Category, Product, Cart, Order, OrderItem
from django.shortcuts import get_object_or_404,redirect

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
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    return JsonResponse({
        'quantity': cart_item.quantity
    })

def remove_from_cart(request, product_id):
    Cart.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart')


def decrease_quantity(request, product_id):
    cart_item = Cart.objects.get(user=request.user, product_id=product_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    # First order discount
    is_first_order = not Order.objects.filter(user=request.user).exists()
    discount = total * 0.10 if is_first_order else 0
    final_total = total - discount

    context = {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total,
    }
    return render(request, 'payment_options.html', context)


def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)

    is_first_order = not Order.objects.filter(user=request.user).exists()
    discount = total * 0.10 if is_first_order else 0
    final_total = total - discount

    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total
    })
    
def increase_quantity(request, product_id):
    cart_item = Cart.objects.get(user=request.user, product_id=product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def update_cart(request, product_id, change):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    change = int(change)
    cart_item.quantity += change

    if cart_item.quantity <= 0:
        cart_item.delete()
        return JsonResponse({
            'quantity': 0,
            'deleted': True
        })

    cart_item.save()

    return JsonResponse({
        'quantity': cart_item.quantity,
        'deleted': False
    })

def place_order(request):
    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('cart')
        total = sum(item.product.price * item.quantity for item in cart_items)

        is_first_order = not Order.objects.filter(user=request.user).exists()
        discount = total * 0.10 if is_first_order else 0
        final_total = total - discount

        order = Order.objects.create(
            user=request.user,
            total=total,
            discount=discount,
            final_total=final_total,
            payment_method=payment_method
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()

        return redirect('order_history')

