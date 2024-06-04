from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CategoryForm, ProductForm, CheckoutForm
from .models import Product, Category, Cart, CartItem, Order, OrderItem

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
            return redirect('django_shop_app:admin_panel')
    else:
        form = CategoryForm()
    return render(request, 'django_shop_app/add_category.html', {'form': form})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('django_shop_app:admin_panel')
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

def admin_panel(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'django_shop_app/admin_panel.html', context)

def product_list(request):
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'django_shop_app/product_list.html', context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('django_shop_app:admin_panel')
    else:
        form = ProductForm(instance=product)
    return render(request, 'django_shop_app/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('django_shop_app:admin_panel')

@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('django_shop_app:cart')

@login_required(login_url='/login/')
def cart(request):
    categories = Category.objects.all()

    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_price = 0
    for item in cart_items:
        item.total_price = item.quantity * item.product.price
        total_price += item.total_price
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'categories': categories
    }
    return render(request, 'django_shop_app/cart.html', context)

def remove_from_cart(request, product_id):
    cart_item = CartItem.objects.get(cart=request.user.cart, product_id=product_id)
    cart_item.delete()
    return redirect('django_shop_app:cart')

@login_required(login_url='/login/')
def checkout(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart_items = CartItem.objects.filter(cart=request.user.cart)
            if cart_items:
                order = Order(
                    user=request.user,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    address=form.cleaned_data['address'],
                    phone_number=form.cleaned_data['phone_number']
                )
                order.save()

                for cart_item in cart_items:
                    OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

                cart_items.delete()

                return redirect('django_shop_app:order_confirmation')
            else:
                return redirect('django_shop_app:cart')
    else:
        form = CheckoutForm()
    return render(request, 'django_shop_app/checkout.html', {'form': form, 'categories': categories})

def order_confirmation(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    return render(request, 'django_shop_app/order_confirmation.html', context)

def order_list(request):
    orders = Order.objects.all()

    for order in orders:
        total_price = 0
        for order_item in order.orderitem_set.all():
            total_price += order_item.product.price * order_item.quantity
        order.total_price = total_price

    context = {'orders': orders}
    return render(request, 'django_shop_app/order_list.html', context)

def order_details(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_items = order.orderitem_set.all()

    total_price = sum(item.product.price * item.quantity for item in order_items)

    context = {'order': order, 'order_items': order_items, 'total_price': total_price}
    return render(request, 'django_shop_app/order_details.html', context)