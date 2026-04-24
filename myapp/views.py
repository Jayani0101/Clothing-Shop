from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from .forms import CustomUserCreationForm
from shop.models import Product, Category, Favorite

@never_cache
def home(request):
    categories = Category.objects.all()
    # Use is_latest field to get latest products (up to 6)
    latest_products = Product.objects.filter(is_latest=True)[:6]
    search_query = request.GET.get('q', '')
    search_results = None
    if search_query:
        search_results = Product.objects.filter(name__icontains=search_query)
    
    show_banner = request.session.pop('show_welcome_banner', False)
    is_new_user = request.session.pop('new_registration', False)
    
    favorited_ids = []
    if request.user.is_authenticated:
        favorited_ids = request.user.favorite_set.values_list('product_id', flat=True)
    return render(request, 'home.html', {
        'categories': categories,
        'latest_products': latest_products,
        'search_query': search_query,
        'search_results': search_results,
        'show_banner': show_banner,
        'is_new_user': is_new_user,
        'favorited_ids': favorited_ids,
    })

@login_required
@require_POST
def toggle_favorite(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True
    return JsonResponse({'is_favorited': is_favorited})

@login_required
def favorites(request):
    favorite_products = Product.objects.filter(favorite__user=request.user)
    return render(request, 'favorites.html', {'products': favorite_products})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['show_welcome_banner'] = True
            request.session['new_registration'] = True
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['show_welcome_banner'] = True
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile(request):
    return render(request, 'profile.html')

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})

@never_cache
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(name__icontains=search_query)
    favorited_ids = []
    if request.user.is_authenticated:
        favorited_ids = request.user.favorite_set.values_list('product_id', flat=True)
    return render(request, 'category_products.html', {
        'category': category,
        'products': products,
        'search_query': search_query,
        'favorited_ids': favorited_ids,
    })

@never_cache
def all_products(request):
    products = Product.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(name__icontains=search_query)
    favorited_ids = []
    if request.user.is_authenticated:
        favorited_ids = request.user.favorite_set.values_list('product_id', flat=True)
    return render(request, 'all_products.html', {
        'products': products,
        'categories': Category.objects.all(),
        'search_query': search_query,
        'favorited_ids': favorited_ids,
    })

def autocomplete(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query)[:10]
        results = [{'name': p.name} for p in products]
    else:
        results = []
    return JsonResponse(results, safe=False)

# New view for all latest products
@never_cache
def latest_products_view(request):
    products = Product.objects.filter(is_latest=True)
    return render(request, 'latest_products.html', {'products': products})
