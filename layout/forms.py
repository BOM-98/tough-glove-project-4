from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput

from .models import *


class CreateUserForm(UserCreationForm):
    """
    A form for creating new users with enhanced field widgets.

    Inherits from Django's UserCreationForm to handle user registration.

    Attributes:
    - password1 (CharField): Field for the user's password.
    - password2 (CharField): Field for confirming the user's password.

    The Meta class:
    - model (User): Specifies the User model to which the form is linked.
    - fields (list): Defines the fields included in the form
    ('first_name', 'last_name', 'username', 'email').
    - widgets (dict): Customizes the widgets for 'username',
    'first_name', 'last_name', and 'email' fields.

    The __init__ method ensures all specified fields are required.
    """
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control item'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password',
                'class': 'form-control item'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Username',
                    'class': 'form-control item'}),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name',
                    'class': 'form-control item'}),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Last Name',
                    'class': 'form-control item'}),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Email',
                    'class': 'form-control item'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for fieldname in ['username',
                          'email',
                          'first_name',
                          'last_name',
                          'password1',
                          'password2']:
            self.fields[fieldname].required = True


class UpdateUserForm(forms.ModelForm):
    """
    A form for updating existing user details.

    This form is based on Django's ModelForm and
    is linked to the User model.

    Attributes:
    - Meta class:
        - model (User): Specifies the User model
        to which the form is linked.
        - fields (list): Defines the fields included
        in the form ('first_name', 'last_name',
        'username', 'email').
        - widgets (dict): Customizes the appearance
        of the 'username', 'first_name', 'last_name',
        and 'email' fields.

    The __init__ method of this class ensures that
    all the specified fields are set as required, meaning
    they must be filled out when the form is submitted.
    """
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email']
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Username',
                       'class': 'form-control item'}),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'First Name',
                       'class': 'form-control item'}),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Last Name',
                       'class': 'form-control item'}),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Email',
                       'class': 'form-control item'}),
        }

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'first_name', 'last_name']:
            self.fields[fieldname].required = True


class CreateClassForm(forms.ModelForm):
    """
    A form for creating new class entries in the system.

    This form is based on Django's ModelForm
    and is linked to the Classes model.

    Attributes:
    - Meta class:
        - model (Classes): Specifies the Classes model
        to which the form is linked.
        - fields (list): Defines the fields included in
        the form ('class_name', 'class_description', 'class_type',
          'class_date', 'class_start_time', 'class_end_time',
          'slots_available').
        - widgets (dict): Customizes the appearance and
        functionality of the form fields, including text inputs,
          textarea, select dropdown, date picker,
          and time picker inputs.

    The __init__ method of this class ensures that certain
    fields ('class_type', 'class_date', 'class_start_time',
    'class_end_time', 'slots_available') are set as required,
    meaning they must be filled out when the form is submitted.
    """
    class Meta:
        model = Classes
        fields = ['class_name',
                  'class_description',
                  'class_type', 'class_date',
                  'class_start_time',
                  'class_end_time',
                  'slots_available']
        widgets = {
            'class_name': forms.TextInput(
                attrs={'placeholder': 'Class Name',
                       'class': 'form-control item'}),
            'class_description': forms.Textarea(
                attrs={'placeholder': 'Class Description',
                       'class': 'form-control item'}),
            'class_type': forms.Select(
                attrs={'placeholder': 'Class Type',
                       'class': 'form-control item'}),
            'class_date': DatePickerInput(
                options={"format": 'DD/MM/YY'},
                attrs={'placeholder': 'Class Date',
                       'class': 'form-control item'}),
            'class_start_time': TimePickerInput(
                options={"format": 'HH:mm',
                         "stepping": 15, },
                attrs={'placeholder': 'Class Start Time',
                       'class': 'form-control item'}),
            'class_end_time': TimePickerInput(
                options={"format": 'HH:mm',
                         "stepping": 15, },
                attrs={'placeholder': 'Class End Time',
                       'class': 'form-control item'},
                range_from='class_start_time'),
            'slots_available': forms.NumberInput(
                attrs={'placeholder': 'Slots Available',
                       'class': 'form-control item'}),
        }

        def __init__(self, *args, **kwargs):
            super(CreateClassForm, self).__init__(*args, **kwargs)
            for fieldname in ['class_type',
                              'class_date',
                              'class_start_time',
                              'class_end_time',
                              'slots_available']:
                self.fields[fieldname].required = True


class UpdateClassForm(forms.ModelForm):
    """
    A form for updating existing class entries in the system.

    This form, derived from Django's ModelForm, is linked to the
    Classes model and is used for updating the details of existing
    class entries.

    Attributes:
    - Meta class:
        - model (Classes): Specifies the Classes model to which the
        form is linked.
        - fields (list): Defines the fields included in the form
        ('class_name', 'class_description', 'class_type',
          'class_date', 'class_start_time', 'class_end_time',
          'slots_available').
        - widgets (dict): Customizes the appearance and functionality
        of the form fields, including text inputs,
          textarea, select dropdown, date picker, and time picker inputs.

    The form's widgets are designed to provide a user-friendly
    interface for data input and modification. The date and time pickers,
    in particular, ensure that class schedules are updated
    accurately and efficiently.
    """
    class Meta:
        model = Classes
        fields = ['class_name',
                  'class_description',
                  'class_type',
                  'class_date',
                  'class_start_time',
                  'class_end_time',
                  'slots_available']
        widgets = {
            'class_name': forms.TextInput(
                attrs={'placeholder': 'Class Name',
                       'class': 'form-control item'}),
            'class_description': forms.Textarea(
                attrs={'placeholder': 'Class Description',
                       'class': 'form-control item'}),
            'class_type': forms.Select(
                attrs={'placeholder': 'Class Type',
                       'class': 'form-control item'}),
            'class_date': DatePickerInput(
                format='%Y-%m-%d',
                attrs={'placeholder': 'Class Date',
                       'class': 'form-control item'}),
            'class_start_time': TimePickerInput(
                options={"format": 'HH:mm', "stepping": 15, },
                attrs={'placeholder': 'Class Start Time',
                       'class': 'form-control item'}),
            'class_end_time': TimePickerInput(
                options={"format": 'HH:mm', "stepping": 15, },
                attrs={'placeholder': 'Class End Time',
                       'class': 'form-control item'},
                range_from='class_start_time'),
            'slots_available': forms.NumberInput(
                attrs={'placeholder': 'Slots Available',
                       'class': 'form-control item'}),
        }


class BookingForm(forms.ModelForm):
    """
    A form for creating and managing bookings for classes.

    This form, derived from Django's ModelForm, is linked
    to the Bookings model and is primarily used for creating
    new bookings for classes.

    Attributes:
    - Meta class:
        - model (Bookings): Specifies the Bookings model
        to which the form is linked.
        - fields (list): Defines the fields included in the
        form ('class_id', 'user').
        - widgets (dict): Customizes the appearance and functionality
        of the form fields. Both fields are set as
          hidden inputs to prevent direct user manipulation.

    The hidden inputs for 'class_id' and 'user' ensure that the booking
    details are securely and accurately captured, typically based on the
    context of the user's actions (e.g., a user booking a specific class).
    This form is crucial in the process of reserving slots for classes,
    helping to manage the availability and scheduling of classes efficiently.
    """
    class Meta:
        model = Bookings
        fields = ['class_id', 'user']
        widgets = {
            'class_id': forms.HiddenInput(
                attrs={'placeholder': 'Class',
                       'class': 'form-control item'}),
            'user': forms.HiddenInput(
                attrs={'placeholder': 'User',
                       'class': 'form-control item'}),
        }
