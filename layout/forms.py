from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Classes, Bookings

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control item'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control item'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control item'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control item'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control item'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control item'}),
        }

