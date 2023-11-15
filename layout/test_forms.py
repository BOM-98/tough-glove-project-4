from django.test import TestCase
from django.contrib.auth.models import User
from .forms import CreateUserForm, UpdateUserForm, CreateClassForm, UpdateClassForm, BookingForm

class TestUserCreationForm(TestCase):
    
    # form field all fields are valid test
    def test_form_valid(self):
            form_data = {
                'first_name': 'New',
                'last_name': 'User',
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'complexpassword123**',
                'password2': 'complexpassword123**'
            }
            form = CreateUserForm(data=form_data)
            self.assertTrue(form.is_valid())
    
    # form field missing first name test
    def test_form_invalid_missing_first_name(self):
            form_data = {
                'last_name': 'User',
                'username': 'newuser',
                'email': 'newuser@example2.com',
                'password1': 'complexpassword123**',
                'password2': 'complexpassword123**',
            }
            form = CreateUserForm(data=form_data)
            self.assertFalse(form.is_valid())
            
    # form field missing username test
    def test_form_invalid_missing_username(self):
            form_data = {
                'first_name': 'New',
                'last_name': 'User',
                'email': 'newuser@example2.com',
                'password1': 'complexpassword123**',
                'password2': 'complexpassword123**',
            }
            form = CreateUserForm(data=form_data)
            self.assertFalse(form.is_valid())
            
    # form field missing email test
    def test_form_invalid_missing_email(self):
        form_data = {
                'first_name': 'New',
                'last_name': 'User',
                'username': 'newuser',
                'password1': 'complexpassword123**',
                'password2': 'complexpassword123**',
            }
        form = CreateUserForm(data=form_data)
        self.assertFalse(form.is_valid())


    # Form Field Unique Username Tests
    def test_form_invalid_duplicate_username(self):
        User.objects.create_user(
            first_name = "New", 
            last_name  = "User", 
            username='newuser',
            email='example@email1.com',
            password='complexpassword123**',
            )
        
        form_data = {
                'first_name': 'New',
                'last_name': 'User',
                'username': 'newuser',
                'email': 'example@email2.com',
                'password':'complexpassword123**',
                'password2':'complexpassword123**',
        }
        form = CreateUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        
    
    #Form Field Unique Email Tests
    def test_form_invalid_duplicate_email(self):
        User.objects.create_user(
            first_name = "New", 
            last_name  = "User", 
            username='newuser1',
            email='example@email.com',
            password='complexpassword123**',
            )
        
        form_data = {
                'first_name': 'New',
                'last_name': 'User',
                'username': 'newuser2',
                'email': 'example@email.com',
                'password1':'complexpassword123**',
                'password2':'complexpassword123**',
        }
        form = CreateUserForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    # Different Passwords Validation Tests
    def test_form_different_passwords(self):
        form_data = {
                'first_name': 'New',
                'last_name': 'User',
                'username': 'newuser',
                'email': 'example@email.com',
                'password1':'complexpassword123**',
                'password2':'complexpassword12**',
        }
        form = CreateUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

class TestUpdateUserForm(TestCase):
    
    # form field all fields are valid test
    def test_form_valid(self):
            User.objects.create_user(
            first_name = "First", 
            last_name  = "User", 
            username='newuser12',
            email='example1@email.com',
            password='complexpassword123**',
            )
            
            form_data = {
                'first_name': 'New',
                'last_name': 'User',
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'complexpassword123**',
                'password2': 'complexpassword123**'
            }
            form = UpdateUserForm(data=form_data)
            self.assertTrue(form.is_valid())
    
    # form field missing first name test
    def test_form_invalid_missing_first_name(self):
            User.objects.create_user(
            first_name = "First", 
            last_name  = "User", 
            username='newuser12',
            email='example1@email.com',
            password='complexpassword123**',
            )
            
            form_data = {
                'last_name': 'User',
                'username': 'newuser',
                'email': 'newuser@example2.com'
            }
            form = UpdateUserForm(data=form_data)
            self.assertFalse(form.is_valid())
    
    # form field missing last name test
    def test_form_invalid_missing_first_name(self):
            User.objects.create_user(
            first_name = "First", 
            last_name  = "User", 
            username='newuser12',
            email='example1@email.com',
            password='complexpassword123**',
            )
            
            form_data = {
                'first_name': 'New',
                'username': 'newuser',
                'email': 'newuser@example2.com'
            }
            form = UpdateUserForm(data=form_data)
            self.assertFalse(form.is_valid())
            
    # form field missing username test
    def test_form_invalid_missing_username(self):
            User.objects.create_user(
            first_name = "First", 
            last_name  = "User", 
            username='newuser12',
            email='example1@email.com',
            password='complexpassword123**',
            )
            
            form_data = {
                'first_name': 'New',
                'last_name': 'User',
                'email': 'newuser@example2.com',
            }
            form = UpdateUserForm(data=form_data)
            self.assertFalse(form.is_valid())
            
    # form field missing email test
    def test_form_invalid_missing_email(self):
        User.objects.create_user(
            first_name = "First", 
            last_name  = "User", 
            username='newuser12',
            email='example1@email.com',
            password='complexpassword123**',
            )
        
        form_data = {
                'first_name': 'New',
                'last_name': 'User',
                'username': 'newuser',
            }
        form = UpdateUserForm(data=form_data)
        self.assertFalse(form.is_valid())
    