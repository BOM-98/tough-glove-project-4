# Standard library imports

# Related third-party imports
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Local application/library specific imports
from .forms import CreateUserForm
from layout.booking_functions.availability import get_available_classes



# Create your views here.
def homepage(request):
    return render(request, "layout/homepage.html")

def register_view(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account created successfully for " + user)
            return redirect('login')
    
    context = {'form': form}
    return render(request, "accounts/register.html", context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        # Check the password if the user exists
        if user is not None and user.check_password(password):
            # Manually authenticate the user, then login
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, "Email or password is incorrect")

    context = {}
    return render(request, "accounts/login.html", context)

def available_classes_view(request):
    available_classes = get_available_classes()
    return render(request, 'available_classes.html', {'available_classes': available_classes})
