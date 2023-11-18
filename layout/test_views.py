from django.test import TestCase
from .models import *
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class TestRegisterLoginViews(TestCase):
    
    def setUp(self):
        """
        Set up the test environment by creating a user and a member object.
        """
        Group.objects.create(name='member')
        
        User.objects.create_user(
            username='testuser1',
            first_name='Test1',
            last_name='User1',
            email = 'testuseremail@email.com',
            password='testpassword332',
        )
    
    def test_homepage_view(self):
        """
        Test the homepage view to ensure it returns a successful response and uses the correct template.

        This test method checks if the homepage view is functioning correctly. It sends a GET request
        to the root URL ('/') and then asserts two conditions:
        1. The response status code is 200, indicating a successful HTTP response.
        2. The correct template ('layout/homepage.html') is used to render the homepage.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'layout/homepage.html' template is used in the response.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'layout/homepage.html')
    
    def test_register_view(self):
        """
        Test the register view to ensure it returns a successful response and uses the correct template.
        
        This test method checks if the register view is functioning correctly. It sends a GET request
        to the register URL ('/register/') and then asserts two conditions:
        1. The response status code is 200, indicating a successful HTTP response.
        2. The correct template ('accounts/register.html') is used to render the register page.
        
        Assertions: 
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'accounts/register.html' template is used in the response.
        """
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        
    def test_can_register_user(self):
        """
        Test that a user can be registered.
        
        This test method checks if a user can be registered. It sends a POST request to the register URL
        ('/register/') with the required user details and then asserts three conditions:
        1. The response status code is 302, indicating a successful HTTP response.
        2. The user is redirected to the login page.
        3. The user is created in the database.
        """
        
        response = self.client.post('/register/', {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testemail@gmail.com',
            'password1': 'testpassword332',
            'password2': 'testpassword332',
        }, follow=True)
        
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200)
        existing_items = User.objects.filter(username='testuser')
        self.assertEqual(existing_items.count(), 1)
        
    def test_login_view(self):
        """
        Test the login view to ensure it returns a successful response and uses the correct template.
        
        This test method checks if the login view is functioning correctly. It sends a GET request
        to the register URL ('/login/') and then asserts two conditions:
        1. The response status code is 200, indicating a successful HTTP response.
        2. The correct template ('accounts/login.html') is used to render the login page.
        
        Assertions: 
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'accounts/login.html' template is used in the response.
        """
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
    
    def test_can_login_user(self):
        """
        Test that a user can login.
        
        This test method checks if a user can login. It sends a POST request to the login URL
        ('/login/') with the required user details and then asserts two conditions:
        1. The response status code is 302, indicating a successful HTTP response.
        2. The user is redirected to the homepage.
        """
        
        response = self.client.post('/login/', {
            'email': 'testuseremail@email.com',
            'password': 'testpassword332',
        })
        
        self.assertRedirects(response, '/')

class TestMemberViews(TestCase):
    
    def setUp(self):
        """
        Set up the test environment by creating a user and a member object.
        
        This set up method creates a user and a member object. It also creates a group called 'member'
        and adds the user to the group.
        The user is then logged in.
        """
        Group.objects.create(name='member')
        
        self.user = User.objects.create_user(
            username='testuser1',
            first_name='Test1',
            last_name='User1',
            email = 'testuseremail@email.com',
            password='testpassword332',
        )
        
        self.user.groups.add(Group.objects.get(name='member'))
        self.user.save()
        
        response = self.client.post('/login/', {
            'email': 'testuseremail@email.com',
            'password': 'testpassword332',
        })
        
    def test_logout_view(self): 
        """
        This test method checks if the logout view is functioning correctly. It sends a GET request
        to the logout URL ('/logout/') and then asserts two conditions:
        1. The response status code is 302, indicating a successful HTTP response.
        2. The user is redirected to the homepage.
        """
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        
    def test_available_classes_view(self):
        """
        Test the available classes view to ensure it returns a successful response.
        
        This test method checks if the available classes view is functioning correctly. It sends a GET request
        to the available classes URL ('/available_classes/') and then asserts:
        1. The response status code is 200, indicating a successful HTTP response.
        
        Assertions: 
        - Asserts that the HTTP response status code is 200.
        """
        response = self.client.get('/available_classes/')
        self.assertEqual(response.status_code, 200)
        
    def test_profile_view(self):
        """
        Test the profile view to ensure it returns a successful response and uses the correct template.
        
        This test method checks if the profile view is functioning correctly. It sends a GET request
        to the profile URL ('/profile/') and then asserts two conditions:
        1. The response status code is 200, indicating a successful HTTP response.
        2. The correct template ('layout/profile.html') is used to render the profile page.
        
        Assertions: 
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'layout/profile.html' template is used in the response.
        """
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        
    def test_update_member_view(self):
        """
        Test the update member view to ensure it returns a successful response and uses the correct template.
        
        This test method checks if the update member view is functioning correctly. It sends a GET request
        to the update member URL ('/update_member/') and then asserts two conditions:
        1. The response status code is 200, indicating a successful HTTP response.
        2. The correct template ('accounts/update_member.html') is used to render the update member page.
        
        Assertions: 
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'layout/update_member.html' template is used in the response.
        """
        response = self.client.get(f'/update_member/{self.user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/update_member.html')
        
    def test_can_update_profile(self):
        """
        Test that a user can update their profile.
        
        This test method checks if a user can update their profile. It sends a POST request to the profile URL
        ('/profile/') with the required user details and then asserts two conditions:
        1. The response status code is 302, indicating a successful HTTP response.
        2. The user is redirected to the profile page.
        """
            
        response = self.client.post(f'/update_member/{self.user.id}/', {
            'username': 'testuser1',
            'first_name': 'Test1',
            'last_name': 'User1',
            'email': 'email45@gmail.com'
        })
        
        self.assertRedirects(response, '/profile/')
        existing_items = User.objects.filter(email='email45@gmail.com')
        self.assertEqual(existing_items.count(), 1)
        
        
        
        
class TestAdminViews(TestCase):
    
    def setUp(self):
        """
        Set up the test environment by creating a user and a member object.
        
        This set up method creates a user and a member object. It also creates a group called 'admin'
        and adds the user to the group.
        The user is then logged in.
        """
        Group.objects.create(name='admin')
        
        self.user = User.objects.create_user(
            username='testuser1',
            first_name='Test1',
            last_name='User1',
            email = 'testemail@gmail.com',
            password = 'testpassword332',
        )
        
        self.user.groups.add(Group.objects.get(name='admin'))
        self.user.save()
        
        response = self.client.post('/login/', {
            'email': 'testemail@gmail.com',
            'password': 'testpassword332',
        })
    
    def test_members_view(self):
        """
        Test the members view to ensure it returns a successful response and uses the correct template.
        
        This test method checks if the members view is functioning correctly. It sends a GET request
        to the members URL ('/members/') and then asserts two conditions:
        1. The response status code is 200, indicating a successful HTTP response.
        2. The correct template ('accounts/members.html') is used to render the members page.
        
        Assertions: 
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'accounts/members.html' template is used in the response.
        """
        
        self.assertTrue(self.client.session['_auth_user_id'], "User is not logged in.")
        response = self.client.get(reverse('members'))
        if response.status_code == 302:
            response = self.client.get(response['Location'], follow=True)
            print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/members.html')
        