from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm

def index(request):
    return render(request, 'django_shop_app/index.html')

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