from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Customer, Product, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . forms import RegisterForm
from django import forms
def index(request):
    return HttpResponse("Welcome to Crop Planet!")

def category(request, foo='something'):
    foo=foo.replace('-', ' ')
    try:
        category = Category.objects.get(name="something")
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'category': category, 'products': products})
    except:
        messages.error(request, "Category does not exist.")
        return redirect('home')


def products(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'product': product})

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  
        
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully.")   
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            form = RegisterForm()
            messages.error(request, "Registration failed. Please correct the errors below.")
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
        
# Create your views here.
