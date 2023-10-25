from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput

from .models import *

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
        
class UpdateUserForm(forms.ModelForm):
    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control item'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control item'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control item'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control item'}),
        }
        
class CreateClassForm(forms.ModelForm):
    class Meta: 
        model = Classes
        fields = ['class_name', 'class_description', 'class_type', 'class_date', 'class_start_time', 'class_end_time', 'slots_available']
        widgets = {
            'class_name': forms.TextInput(attrs={'placeholder': 'Class Name', 'class': 'form-control item'}),
            'class_description': forms.Textarea(attrs={'placeholder': 'Class Description', 'class': 'form-control item'}),
            'class_type': forms.Select(attrs={'placeholder': 'Class Type', 'class': 'form-control item'}),
            'class_date': DatePickerInput(format='%Y-%m-%d', attrs={'placeholder': 'Class Date', 'class': 'form-control item'}),
            'class_start_time': TimePickerInput(format='%H:%M', attrs={'placeholder': 'Class Start Time', 'class': 'form-control item'}),
            'class_end_time': TimePickerInput(format='%H:%M', attrs={'placeholder': 'Class End Time', 'class': 'form-control item'}),
            'slots_available': forms.NumberInput(attrs={'placeholder': 'Slots Available', 'class': 'form-control item'}),
        }
        
class UpdateClassForm(forms.ModelForm):
    class Meta: 
        model = Classes
        fields = ['class_name', 'class_description', 'class_type', 'class_date', 'class_start_time', 'class_end_time', 'slots_available']
        widgets = {
            'class_name': forms.TextInput(attrs={'placeholder': 'Class Name', 'class': 'form-control item'}),
            'class_description': forms.Textarea(attrs={'placeholder': 'Class Description', 'class': 'form-control item'}),
            'class_type': forms.Select(attrs={'placeholder': 'Class Type', 'class': 'form-control item'}),
            'class_date': DatePickerInput(format='%Y-%m-%d', attrs={'placeholder': 'Class Date', 'class': 'form-control item'}),
            'class_start_time': TimePickerInput(format='%H:%M', attrs={'placeholder': 'Class Start Time', 'class': 'form-control item'}),
            'class_end_time': TimePickerInput(format='%H:%M', attrs={'placeholder': 'Class End Time', 'class': 'form-control item'}),
            'slots_available': forms.NumberInput(attrs={'placeholder': 'Slots Available', 'class': 'form-control item'}),
        }

class BookingForm(forms.ModelForm):
    class Meta: 
        model = Bookings
        fields = ['class_id','user']
        widgets = {
            'class_id': forms.HiddenInput(attrs={'placeholder': 'Class', 'class': 'form-control item'}),
            'user': forms.HiddenInput(attrs={'placeholder': 'User', 'class': 'form-control item'}),
        }