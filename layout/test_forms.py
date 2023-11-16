from django.test import TestCase
from django.contrib.auth.models import User
from .forms import CreateUserForm, UpdateUserForm, CreateClassForm, UpdateClassForm, BookingForm
from .models import *
from datetime import datetime, timedelta

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
            user_instance = User.objects.create_user(
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
            form = UpdateUserForm(data=form_data, instance = user_instance)
            self.assertTrue(form.is_valid())
    
    # form field missing first name test
    def test_form_invalid_missing_first_name(self):
            user_instance =  User.objects.create_user(
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
            form = UpdateUserForm(data=form_data, instance = user_instance)
            self.assertFalse(form.is_valid())
    
    # form field missing last name test
    def test_form_invalid_missing_first_name(self):
            user_instance = User.objects.create_user(
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
            form = UpdateUserForm(data=form_data, instance = user_instance)
            self.assertFalse(form.is_valid())
            
    # form field missing username test
    def test_form_invalid_missing_username(self):
            user_instance = User.objects.create_user(
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
            form = UpdateUserForm(data=form_data, instance = user_instance)
            self.assertFalse(form.is_valid())
            
    # form field missing email test
    def test_form_invalid_missing_email(self):
        user_instance = User.objects.create_user(
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
        form = UpdateUserForm(data=form_data, instance = user_instance)
        self.assertFalse(form.is_valid())
        
class TestCreateClassForm(TestCase):
    
    # form field all fields are valid test
    def test_form_valid_data(self):
        form_data = {
            'class_name': 'Yoga',
            'class_description': 'A relaxing yoga session',
            'class_type': 0,
            'class_date': datetime.now().date(),
            'class_start_time': datetime.now().time(),
            'class_end_time': (datetime.now() + timedelta(hours=1)).time(),
            'slots_available': 10
        }
        form = CreateClassForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    # form field missing class type test
    def test_form_invalid_missing_class_type(self):
        form_data = {
            'class_name': 'Yoga',
            'class_description': 'A relaxing yoga session',
            'class_date': datetime.now().date(),
            'class_start_time': datetime.now().time(),
            'class_end_time': (datetime.now() + timedelta(hours=1)).time(),
            'slots_available': 10
        }
        form = CreateClassForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('class_type', form.errors)
        
    # form field missing class date test
    def test_form_invalid_missing_class_date(self):
        """
        This test to ensures the CREATECLASSFORM is invalid if no CLASS_DATE field is inputed.
        This test creates a form data dictionary without the CLASS_DATE field and
        initializes the CREATECLASSFORM with this data. It then checks two things:
        1. The form is not valid (self.assertFalse(form.is_valid())).
        2. The specific error for 'class_date' is included in the form's errors 
        The absence of class_date should trigger a validation error, making the form invalid.
        """
        form_data = {
            'class_name': 'Yoga',
            'class_description': 'A relaxing yoga session',
            'class_type': 0,
            'class_start_time': datetime.now().time(),
            'class_end_time': (datetime.now() + timedelta(hours=1)).time(),
            'slots_available': 10
        }
        form = CreateClassForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('class_date', form.errors)
        
    # form field missing class start time test
    def test_form_invalid_missing_class_start_time(self):
        """
        This test to ensures the CREATECLASSFORM is invalid if no CLASS_START_TIME field is inputed.
        This test creates a form data dictionary without the CLASS_START_TIME field and
        initializes the CREATECLASSFORM with this data. It then checks two things:
        1. The form is not valid (self.assertFalse(form.is_valid())).
        2. The specific error for 'class_start_time' is included in the form's errors 
        The absence of class_start_time should trigger a validation error, making the form invalid.
        """
        form_data = {
            'class_name': 'Yoga',
            'class_description': 'A relaxing yoga session',
            'class_type': 0,
            'class_date': datetime.now().date(),
            'class_end_time': (datetime.now() + timedelta(hours=1)).time(),
            'slots_available': 10
        }
        form = CreateClassForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('class_start_time', form.errors)
        
    def test_form_invalid_missing_class_end_time(self):
        """
        This test to ensures the CREATECLASSFORM is invalid if no CLASS_END_TIME field is inputed.
        This test creates a form data dictionary without the CLASS_END_TIME field and
        initializes the CREATECLASSFORM with this data. It then checks two things:
        1. The form is not valid (self.assertFalse(form.is_valid())).
        2. The specific error for 'class_end_time' is included in the form's errors 
        The absence of class_end_time should trigger a validation error, making the form invalid.
        """
        form_data = {
            'class_name': 'Yoga',
            'class_description': 'A relaxing yoga session',
            'class_type': 0,
            'class_date': datetime.now().date(),
            'class_start_time': datetime.now().time(),
            'slots_available': 10
        }
        form = CreateClassForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('class_end_time', form.errors)
        
    def test_form_invalid_missing_slots_available(self):
        """
        This test to ensures the CREATECLASSFORM is invalid if no SLOTS_AVAILABLE field is inputed.
        This test creates a form data dictionary without the SLOTS_AVAILABLE field and
        initializes the CREATECLASSFORM with this data. It then checks two things:
        1. The form is not valid (self.assertFalse(form.is_valid())).
        2. The specific error for 'slots_available' is included in the form's errors
        The absence of slots_available should trigger a validation error, making the form invalid.
        """
        form_data = {
            'class_name': 'Yoga',
            'class_description': 'A relaxing yoga session',
            'class_type': 0,
            'class_date': datetime.now().date(),
            'class_start_time': datetime.now().time(),
            'class_end_time': (datetime.now() + timedelta(hours=1)).time(),
        }
        form = CreateClassForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('slots_available', form.errors)
        
class TestUpdateClassForm(TestCase):
    
    def test_form_valid_data(self):
        """
        This test to ensures the UPDATECLASSFORM is valid if no fields are excluded.
        This test creates a class instance and creates a form data dictionary without 
        all fields included and initializes the CREATECLASSFORM with this data. 
        It then checks:
        1. The form is valid (self.assertTrue(form.is_valid()))
        The inclusion of all fields should, ensure the form valid.
        """
        class_instance = Classes.objects.create(
            class_name = 'Yoga',
            class_description = 'A relaxing yoga session',
            class_type = 0,
            class_date = datetime.now().date(),
            class_start_time = datetime.now().time(),
            class_end_time = (datetime.now() + timedelta(hours=1)).time(),
            slots_available = 10
        )
        
        form_data = {
            'class_name': 'Yoga',
            'class_description': 'A relaxing yoga session',
            'class_type': 0,
            'class_date': datetime.now().date(),
            'class_start_time': datetime.now().time(),
            'class_end_time': (datetime.now() + timedelta(hours=1)).time(),
            'slots_available': 10,
        }

        form = UpdateClassForm(data=form_data, instance = class_instance)
        self.assertTrue(form.is_valid())
        if form.is_valid():
            instance = form.save()
            self.assertIsNotNone(instance)
            
    def test_form_invalid_missing_class_type(self):
        """
        This test to ensures the UPDATECLASSFORM is invalid if no CLASS_TYPE field is inputed.
        This test creates a class instance and creates a form data dictionary without 
        the CLASS_TYPE field and initializes the CREATECLASSFORM with this data. 
        It then checks two things:
        1. The form is not valid (self.assertFalse(form.is_valid())).
        2. The specific error for 'class_type' is included in the form's errors 
        The absence of class_type should trigger a validation error, making the form invalid.
        """
        class_instance = Classes.objects.create(
            class_name = 'Yoga',
            class_description = 'A relaxing yoga session',
            class_type = 0,
            class_date = datetime.now().date(),
            class_start_time = datetime.now().time(),
            class_end_time = (datetime.now() + timedelta(hours=1)).time(),
            slots_available = 10
        )
        
        form_data = {
            'class_name': 'Yoga',
            'class_description': 'A relaxing yoga session',
            'class_date': datetime.now().date(),
            'class_start_time': datetime.now().time(),
            'class_end_time': (datetime.now() + timedelta(hours=1)).time(),
            'slots_available': 10,
        }

        form = UpdateClassForm(data=form_data, instance = class_instance)
        self.assertFalse(form.is_valid())
        self.assertIn('class_type', form.errors)
        
    def test_form_invalid_missing_class_date(self):
        """
        This test to ensures the UPDATECLASSFORM is invalid if no CLASS_DATE field is inputed.
        This test creates a class instance and creates a form data dictionary without
        the CLASS_DATE field and initializes the CREATECLASSFORM with this data.
        It then checks two things:
        1. The form is not valid (self.assertFalse(form.is_valid())).
        2. The specific error for 'class_date' is included in the form's errors
        The absence of class_date should trigger a validation error, making the form invalid.
        """
        class_instance = Classes.objects.create(
            class_name = 'Yoga',
            class_description = 'A relaxing yoga session',
            class_type = 0,
            class_date = datetime.now().date(),
            class_start_time = datetime.now().time(),
            class_end_time = (datetime.now() + timedelta(hours=1)).time(),
            slots_available = 10
        )
        
        form_data = {
            'class_name': 'Yoga',
            'class_description': 'A relaxing yoga session',
            'class_type': 0,
            'class_start_time': datetime.now().time(),
            'class_end_time': (datetime.now() + timedelta(hours=1)).time(),
            'slots_available': 10,
        }
        
        form = UpdateClassForm(data=form_data, instance = class_instance)
        self.assertFalse(form.is_valid())
        self.assertIn('class_date', form.errors)
    
class TestBookingForm(TestCase):
    
    def test_form_valid_data(self):
        """
        This test to ensures the BOOKINGFORM is valid if no fields are excluded.
        This test creates a class instance and creates a form data dictionary with
        all fields included and initializes the BOOKINGFORM with this data.
        It then checks:
        1. The form is valid (self.assertTrue(form.is_valid()))
        The inclusion of all fields should, ensure the form valid.
        """
        user_instance = User.objects.create_user(
            first_name = "First", 
            last_name  = "User", 
            username='newuser12',
        )
        class_instance = Classes.objects.create(
            class_name = 'Yoga',
            class_description = 'A relaxing yoga session',
            class_type = 0,
            class_date = datetime.now().date(),
            class_start_time = datetime.now().time(),
            class_end_time = (datetime.now() + timedelta(hours=1)).time(),
            slots_available = 10
        )
        form_data = {
            'user': user_instance,
            'class_id': class_instance,
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())
        if form.is_valid():
            instance = form.save()
            self.assertIsNotNone(instance)
            
    def test_form_invalid_missing_user(self):
        """
        This test to ensures the BOOKINGFORM is invalid if no USER field is inputed.
        This test creates a class instance and creates a form data dictionary without
        the USER field and initializes the BOOKINGFORM with this data.
        It then checks two things:
        1. The form is not valid (self.assertFalse(form.is_valid())).
        2. The specific error for 'user' is included in the form's errors
        The absence of user should trigger a validation error, making the form invalid.
        """
        class_instance = Classes.objects.create(
            class_name = 'Yoga',
            class_description = 'A relaxing yoga session',
            class_type = 0,
            class_date = datetime.now().date(),
            class_start_time = datetime.now().time(),
            class_end_time = (datetime.now() + timedelta(hours=1)).time(),
            slots_available = 10
        )
        form_data = {
            'class_id': class_instance,
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('user', form.errors)
        
    def test_form_invalid_missing_class_id(self):
        """
        This test to ensures the BOOKINGFORM is invalid if no CLASS_ID field is inputed.
        This test creates a class instance and creates a form data dictionary without
        the CLASS_ID field and initializes the BOOKINGFORM with this data.
        It then checks two things:
        1. The form is not valid (self.assertFalse(form.is_valid())).
        2. The specific error for 'class_id' is included in the form's errors
        The absence of class_id should trigger a validation error, making the form invalid.
        """
        user_instance = User.objects.create_user(
            first_name = "First", 
            last_name  = "User", 
            username='newuser12',
        )
        form_data = {
            'user': user_instance,
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('class_id', form.errors)
            