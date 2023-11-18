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
        
    def test_can_not_update_other_profile(self):
        """
        Test that a user can't update the profile of other members unless
        they are an admin.
        
        This method checks if a user can update the profile of other members. 
        It creates a second user in the members group to test with. It sends a
        GET request to the update member URL ('/update_member/') with a different user id to their own
        and then asserts two conditions:
        1. The response status code is 302, indicating a redirect.
        2. The user is redirected to the profile page.
        
        Assertions:
        - Asserts that the HTTP response status code is 302.
        - Asserts that the user is redirected to the profile page.
        """
        
        self.other_user = User.objects.create_user(
            username='testuser2',
            first_name='Test2',
            last_name='User2',
            email = 'testuseremail2@email.com',
            password='testpassword3322',
        )
        
        self.other_user.groups.add(Group.objects.get(name='member'))
        self.other_user.save()
        
        response = self.client.get(f'/update_member/{self.other_user.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/profile/')
        
class TestAdminViews(TestCase):
    
    def setUp(self):
        """
        Set up the test environment by creating two users and two groups.
        
        This set up method creates two users and groups. 
        It also creates a group called 'admin' and a group called "member"
        and adds a user to each group.
        The admin user is then logged in.
        """
        Group.objects.create(name='admin')
        Group.objects.create(name='member')
        
        self.user = User.objects.create_user(
            username='testuser1',
            first_name='Test1',
            last_name='User1',
            email = 'testemail@gmail.com',
            password = 'testpassword332',
        )
        
        self.user.groups.add(Group.objects.get(name='admin'))
        self.user.save()
        
        self.other_user = User.objects.create_user(
        username='testuser2',
        first_name='Test2',
        last_name='User2',
        email = 'testuseremail2@email.com',
        password='testpassword3322',
        )
        self.other_user.groups.add(Group.objects.get(name='member'))
        self.other_user.save()
        
        response = self.client.post('/login/', {
            'email': 'testemail@gmail.com',
            'password': 'testpassword332',
        })
    
    def test_members_view(self):
        """
        Test the members view for successful response and correct template usage.

        This test method validates the functionality of the members view. It performs the following steps:
        1. Ensures that a user is logged in by checking the session's '_auth_user_id'.
        2. Sends a GET request to the members URL ('/members/') using Django's `reverse` function for URL resolution.
        3. Handles potential redirection (HTTP 302 response) by following the redirect and fetching the final response.
        This assists in troubleshooting the test in case of redirection.
        4. Asserts two key conditions:
        - The final response status code is 200, indicating a successful HTTP response.
        - The 'accounts/members.html' template is used to render the members page.

        Assertions:
        - Asserts that the user is logged in before making the GET request.
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'accounts/members.html' template is used in the response.

        The test also includes a conditional check for HTTP 302 responses, which are common in cases of redirection. 
        If a redirection occurs, the test follows the redirect and then performs the assertions on the final response.
        This ensures that the test accurately reflects the user's experience when accessing the members view.
        """
        
        self.assertTrue(self.client.session['_auth_user_id'], "User is not logged in.")
        response = self.client.get(reverse('members'))
        if response.status_code == 302:
            response = self.client.get(response['Location'], follow=True)
            print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/members.html')
        
    def test_can_update_other_profile_if_admin(self):
        """
        Test that an admin can update the profile of other members.
         
        This method checks if an admin can update the profile of other members.
        
        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'layout/update_member.html' template is used in the response.
        """
        
        response = self.client.get(f'/update_member/{self.other_user.id}/')
        self.assertEqual(response.status_code, 200)

    def test_delete_member_view(self):
        """
        Test the delete member view to ensure it returns a successful response and uses the correct template.
        
        This test method checks if the delete member view is functioning correctly. It sends a GET request
        to the delete member URL ('/delete_member/') and then asserts two conditions:
        1. The response status code is 200, indicating a successful HTTP response.
        2. The correct template ('accounts/delete_member.html') is used to render the delete member page.
        
        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'accounts/delete_member.html' template is used in the response.
        """
        
        response = self.client.get(f'/delete_member/{self.other_user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/delete_member.html')
    
    
    def test_can_delete_profile(self):
        """
        Test that an admin user can delete a profile.
        
        This test method checks if admin can delete a profile. It sends a POST request to the profile URL
        ('/profile/') with the required user details and then asserts two conditions:
        1. The response status code is 302, indicating a successful HTTP response.
        2. The user is redirected to the homepage.
        """
        
        response = self.client.post(f'/delete_member/{self.other_user.id}/')
        self.assertRedirects(response, '/members/')
        existing_items = User.objects.filter(username='testuser2')
        self.assertEqual(existing_items.count(), 0)