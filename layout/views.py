# Standard library imports

# Related third-party imports
from django.db import models
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

# Local application/library specific imports
from .forms import CreateUserForm
from layout.booking_functions.availability import get_available_classes
from .decorators import unauthenticated_user, allowed_users



# Create your views here.
def homepage(request):
    return render(request, "layout/homepage.html")

@unauthenticated_user
def register_view(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='member')
            user.groups.add(group)
            messages.success(request, "Account created successfully for " + username)
            return redirect('login')

    context = {'form': form}
    return render(request, "accounts/register.html", context)

@unauthenticated_user
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

def logout_user(request):
    logout(request)
    return redirect('homepage')

@login_required(login_url='login')
@allowed_users(allowed_roles=['member', 'admin'])
def available_classes_view(request):
    available_classes = get_available_classes()
    return render(request, 'layout/available_classes.html', {'available_classes': available_classes})
