from django.shortcuts import render
from layout.booking_functions.availability import get_available_classes
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm


# Create your views here.
def homepage(request):
    return render(request, "layout/homepage.html")

def register_view(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    
    context = {'form': form}
    return render(request, "accounts/register.html", context)

def login_view(request):
    context = {}
    return render(request, "accounts/login.html", context)

def available_classes_view(request):
    available_classes = get_available_classes()
    return render(request, 'available_classes.html', {'available_classes': available_classes})
