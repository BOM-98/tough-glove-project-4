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
from .forms import *
from layout.booking_functions.availability import get_available_classes
from .decorators import unauthenticated_user, allowed_users
from .models import *



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

@allowed_users(allowed_roles=['admin'])
def create_member_view(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='member')
            user.groups.add(group)
            messages.success(request, "Account created successfully for " + username)
            return redirect('members')

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

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def members_view(request):
    members = Members.objects.all()
    users = User.objects.all()
    user_count = User.objects.count()
    context = {'members': members, 'users': users, 'user_count': user_count}
    return render(request, 'accounts/members.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['member', 'admin'])
def update_member_view(request, pk):
    user = User.objects.get(id=pk)
    form = UpdateUserForm(instance=user)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('members')
    context = {'form': form, 'user': user}
    return render(request, 'accounts/update_member.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_member_view(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('members')
    context = {'user': user}
    return render(request, 'accounts/delete_member.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admin_dashboard_view(request):
    users = User.objects.all()
    classes = Classes.objects.all()
    members = Members.objects.all()
    user_count = User.objects.count()
    classes_count = Classes.objects.count()
    pt_classes_count = Classes.objects.filter(class_type=1).count()
    group_classes_count = Classes.objects.filter(class_type=0).count()
    available_classes = get_available_classes()
    context = {'users': users, 'classes': classes, 'members': members, 'user_count': user_count, 'classes_count': classes_count, 'pt_classes_count': pt_classes_count, 'group_classes_count': group_classes_count, 'available_classes': available_classes}
    return render(request, 'layout/admin_dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def class_manager_view(request):
    if request.method == 'POST':
        form = CreateClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    classes = Classes.objects.all()
    context = {'classes': classes, 'form' : CreateClassForm()}
    return render(request, 'classes/class_manager.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_class_view(request, pk):
    update_class = Classes.objects.get(id=pk)
    form = UpdateClassForm(request.POST, instance = update_class)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    context = {'class': update_class, 'form' : form}
    return render(request, 'classes/class_manager.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_class_view(request, pk):
    delete_class = Classes.objects.get(id=pk)
    if request.method == 'POST':
        delete_class.delete()
        return redirect('admin_dashboard')
    context = {'class': delete_class}
    return render(request, 'classes/delete_class.html', context)