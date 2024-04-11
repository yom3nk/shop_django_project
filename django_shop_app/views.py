from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CategoryForm, ProductForm
from .models import Product, Category

def index(request):
    categories = Category.objects.all()
    latest_products = Product.objects.order_by('-id')[:3]
    
    context = {
        'categories': categories,
        'products': latest_products,
        'on_home_page': True,
    }

    return render(request, 'django_shop_app/index.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('django_shop_app:index')
    return render(request, 'django_shop_app/login.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('django_shop_app:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'django_shop_app/register.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('django_shop_app:index')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('django_shop_app:index')
    else:
        form = CategoryForm()
    return render(request, 'django_shop_app/add_category.html', {'form': form})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('django_shop_app:index')
    else:
        form = ProductForm()
    return render(request, 'django_shop_app/add_product.html', {'form': form})

def category_products(request, category_id):
    categories = Category.objects.all()
    category_products = Product.objects.filter(category_id=category_id)
    
    context = {
        'categories': categories,
        'products': category_products,
        'on_home_page': False,
    }

    return render(request, 'django_shop_app/index.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()
    return render(request, 'django_shop_app/product.html', {'product': product, 'categories': categories})