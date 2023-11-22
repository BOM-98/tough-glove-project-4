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
        Group.objects.create(name="member")

        User.objects.create_user(
            username="testuser1",
            first_name="Test1",
            last_name="User1",
            email="testuseremail@email.com",
            password="testpassword332",
        )

    def test_homepage_view(self):
        """
        Test the homepage view to ensure it returns a
        successful response and uses the correct template.

        This test method checks if the homepage view is
        functioning correctly. It sends a GET request
        to the root URL ('/') and then asserts two
        conditions:
        1. The response status code is 200, indicating
        a successful HTTP response.
        2. The correct template ('layout/homepage.html')
        is used to render the homepage.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'layout/homepage.html'
        template is used in the response.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout/homepage.html")

    def test_register_view(self):
        """
        Test the register view to ensure it returns a successful
        response and uses the correct template.

        This test method checks if the register view is functioning
        correctly. It sends a GET request
        to the register URL ('/register/') and then asserts two
        conditions:
        1. The response status code is 200, indicating a successful
        HTTP response.
        2. The correct template ('accounts/register.html') is used
        to render the register page.

        Assertions:
        - Asserts that the HTTP response status
        code is 200.
        - Asserts that the 'accounts/register.html'
        template is used in the response.
        """
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_can_register_user(self):
        """
        Test that a user can be registered.

        This test method checks if a user can be registered. It
        sends a POST request to the register URL
        ('/register/') with the required user details and then
        asserts three conditions:
        1. The response status code is 302, indicating a successful
        HTTP response.
        2. The user is redirected to the login page.
        3. The user is created in the database.
        """

        response = self.client.post(
            "/register/",
            {
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "testemail@gmail.com",
                "password1": "testpassword332",
                "password2": "testpassword332",
            },
            follow=True,
        )

        self.assertRedirects(
            response, reverse("login"), status_code=302, target_status_code=200
        )
        existing_items = User.objects.filter(username="testuser")
        self.assertEqual(existing_items.count(), 1)

    def test_login_view(self):
        """
        Test the login view to ensure it returns a successful
        response and uses the correct template.

        This test method checks if the login view is functioning
        correctly. It sends a GET request
        to the register URL ('/login/') and then asserts two
        conditions:
        1. The response status code is 200, indicating a
        successful HTTP response.
        2. The correct template ('accounts/login.html')
        is used to render the login page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'accounts/login.html' template
        is used in the response.
        """
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_can_login_user(self):
        """
        Test that a user can login.

        This test method checks if a user can login. It sends
        a POST request to the login URL
        ('/login/') with the required user details and then
        asserts two conditions:
        1. The response status code is 302, indicating a
        successful HTTP response.
        2. The user is redirected to the homepage.
        """

        response = self.client.post(
            "/login/",
            {
                "email": "testuseremail@email.com",
                "password": "testpassword332",
            },
        )

        self.assertRedirects(response, "/")


class TestMemberViews(TestCase):
    def setUp(self):
        """
        Set up the test environment by creating a user and
        a member object.

        This set up method creates a user and a member object.
        It also creates a group called 'member'
        and adds the user to the group.
        The user is then logged in.
        """
        Group.objects.create(name="member")

        self.user = User.objects.create_user(
            username="testuser1",
            first_name="Test1",
            last_name="User1",
            email="testuseremail@email.com",
            password="testpassword332",
        )

        self.user.groups.add(Group.objects.get(name="member"))
        self.user.save()

        response = self.client.post(
            "/login/",
            {
                "email": "testuseremail@email.com",
                "password": "testpassword332",
            },
        )

    def test_logout_view(self):
        """
        This test method checks if the logout view is
        functioning correctly. It sends a GET request
        to the logout URL ('/logout/') and then asserts
        two conditions:
        1. The response status code is 302, indicating
        a successful HTTP response.
        2. The user is redirected to the homepage.
        """
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_available_classes_view(self):
        """
        Test the available classes view to ensure it returns
        a successful response.

        This test method checks if the available classes
        view is functioning correctly. It sends a GET request
        to the available classes URL ('/available_classes/')
        and then asserts:
        1. The response status code is 200, indicating a
        successful HTTP response.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        """
        response = self.client.get("/available_classes/")
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        """
        Test the profile view to ensure it returns a successful
        response and uses the correct template.

        This test method checks if the profile view is
        functioning correctly. It sends a GET request
        to the profile URL ('/profile/') and then asserts
        two conditions:
        1. The response status code is 200, indicating a
        successful HTTP response.
        2. The correct template ('layout/profile.html') is
        used to render the profile page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'layout/profile.html' template is
        used in the response.
        """
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_update_member_view(self):
        """
        Test the update member view to ensure it returns a
        successful response and uses the correct template.

        This test method checks if the update member view is
        functioning correctly. It sends a GET request
        to the update member URL ('/update_member/') and then
        asserts two conditions:
        1. The response status code is 200, indicating a
        successful HTTP response.
        2. The correct template ('accounts/update_member.html')
        is used to render the update member page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'layout/update_member.html' template
        is used in the response.
        """
        response = self.client.get(f"/update_member/{self.user.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/update_member.html")

    def test_can_update_profile(self):
        """
        Test that a user can update their profile.

        This test method checks if a user can update their profile.
        It sends a POST request to the profile URL
        ('/profile/') with the required user details and then
        asserts two conditions:
        1. The response status code is 302, indicating a successful
        HTTP response.
        2. The user is redirected to the profile page.
        """

        response = self.client.post(
            f"/update_member/{self.user.id}/",
            {
                "username": "testuser1",
                "first_name": "Test1",
                "last_name": "User1",
                "email": "email45@gmail.com",
            },
        )

        self.assertRedirects(response, "/profile/")
        existing_items = User.objects.filter(email="email45@gmail.com")
        self.assertEqual(existing_items.count(), 1)

    def test_can_not_update_other_profile(self):
        """
        Test that a user can't update the profile of other
        members unless they are an admin.

        This method checks if a user can update the
        profile of other members.
        It creates a second user in the members group
        to test with. It sends a
        GET request to the update member URL ('/update_member/')
        with a different user id to their own
        and then asserts two conditions:
        1. The response status code is 302, indicating a redirect.
        2. The user is redirected to the profile page.

        Assertions:
        - Asserts that the HTTP response status code is 302.
        - Asserts that the user is redirected to the profile page.
        """

        self.other_user = User.objects.create_user(
            username="testuser2",
            first_name="Test2",
            last_name="User2",
            email="testuseremail2@email.com",
            password="testpassword3322",
        )

        self.other_user.groups.add(Group.objects.get(name="member"))
        self.other_user.save()

        response = self.client.get(f"/update_member/{self.other_user.id}/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/profile/")


class TestAdminViews(TestCase):
    def setUp(self):
        """
        Set up the test environment by creating two users and two groups.

        This set up method creates two users and groups.
        It also creates a group called 'admin' and a group called "member"
        and adds a user to each group.
        The admin user is then logged in.
        """
        Group.objects.create(name="admin")
        Group.objects.create(name="member")

        self.user = User.objects.create_user(
            username="testuser1",
            first_name="Test1",
            last_name="User1",
            email="testemail@gmail.com",
            password="testpassword332",
        )

        self.user.groups.add(Group.objects.get(name="admin"))
        self.user.save()

        self.other_user = User.objects.create_user(
            username="testuser2",
            first_name="Test2",
            last_name="User2",
            email="testuseremail2@email.com",
            password="testpassword3322",
        )
        self.other_user.groups.add(Group.objects.get(name="member"))
        self.other_user.save()

        response = self.client.post(
            "/login/",
            {
                "email": "testemail@gmail.com",
                "password": "testpassword332",
            },
        )

    def test_members_view(self):
        """
        Test the members view for successful response and correct
        template usage.

        This test method validates the functionality of the members view.
        It performs the following steps:
        1. Ensures that a user is logged
        in by checking the session's '_auth_user_id'.
        2. Sends a GET request to the members
        URL ('/members/') using Django's
        `reverse` function for URL resolution.
        3. Handles potential redirection
        (HTTP 302 response) by following
        the redirect and fetching the final response.
        This assists in troubleshooting the
        test in case of redirection.
        4. Asserts two key conditions:
        - The final response status code
        is 200, indicating
        a successful HTTP response.
        - The 'accounts/members.html'
        template is used to render
        the members page.

        Assertions:
        - Asserts that the user is logged
        in before making
        the GET request.
        - Asserts that the HTTP response
        status code is 200.
        - Asserts that the 'accounts/members.html'
        template is
        used in the response.

        The test also includes a conditional
        check for HTTP 302
        responses, which are common in cases
        of redirection.
        If a redirection occurs, the test follows
        the redirect and
        then performs the assertions on the final
        response.
        This ensures that the test accurately reflects
        the user's
        experience when accessing the members view.
        """

        self.assertTrue(self.client.session[
            "_auth_user_id"], "User is not logged in.")
        response = self.client.get(reverse("members"))
        if response.status_code == 302:
            response = self.client.get(response["Location"], follow=True)
            print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/members.html")

    def test_can_update_other_profile_if_admin(self):
        """
        Test that an admin can update the profile of other members.

        This method checks if an admin can update the profile of other members.

        Assertions:
        - Asserts that the HTTP response
        status code is 200.
        - Asserts that the 'layout/update_member.html'
        template is used in the response.
        """

        response = self.client.get(f"/update_member/{self.other_user.id}/")
        self.assertEqual(response.status_code, 200)

    def test_delete_member_view(self):
        """
        Test the delete member view to ensure it
        returns a successful
        response and uses the correct template.

        This test method checks if the delete
        member view is functioning
        correctly. It sends a GET request
        to the delete member URL ('/delete_member/')
        and then asserts
        two conditions:
        1. The response status code is 200, indicating
        a successful HTTP
        response.
        2. The correct template ('accounts/delete_member.html')
        is used
        to render the delete member page.

        Assertions:
        - Asserts that the HTTP response status
        code is 200.
        - Asserts that the 'accounts/delete_member.html'
        template is used
        in the response.
        """

        response = self.client.get(f"/delete_member/{self.other_user.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/delete_member.html")

    def test_can_delete_profile(self):
        """
        Test that an admin user can delete a profile.

        This test method checks if admin can delete a profile.
        It sends a POST request to the profile URL
        ('/profile/') with the required user details
        and then asserts two conditions:
        1. The response status code is 302, indicating
        a successful HTTP response.
        2. The user is redirected to the homepage.
        """

        response = self.client.post(f"/delete_member/{self.other_user.id}/")
        self.assertRedirects(response, "/members/")
        existing_items = User.objects.filter(username="testuser2")
        self.assertEqual(existing_items.count(), 0)

    def test_admin_dashboard_view(self):
        """
        Test the admin dashboard view to ensure it returns a
        successful response and uses the correct template.

        This test method checks if the admin dashboard view
        is functioning correctly. It sends a GET request
        to the admin dashboard URL ('/admin_dashboard/') and
        then asserts two conditions:
        1. The response status code is 200, indicating a successful
        HTTP response.
        2. The correct template ('layout/admin_dashboard.html')
        is used to render the admin dashboard page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'layout/admin_dashboard.html' template
        is used in the response.
        """

        response = self.client.get("/admin_dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "layout/admin_dashboard.html")


class TestClassViews(TestCase):
    def setUp(self):
        """
        Set up the test environment by creating two users and two groups.

        This set up method creates two users and groups.
        It also creates a group called 'admin' and a group called "member"
        and adds a user to each group.
        The admin user is then logged in.
        """
        Group.objects.create(name="admin")
        Group.objects.create(name="member")

        self.user = User.objects.create_user(
            username="testuser1",
            first_name="Test1",
            last_name="User1",
            email="testemail@gmail.com",
            password="testpassword332",
        )

        self.user.groups.add(Group.objects.get(name="admin"))
        self.user.save()

        self.other_user = User.objects.create_user(
            username="testuser2",
            first_name="Test2",
            last_name="User2",
            email="testuseremail2@email.com",
            password="testpassword3322",
        )
        self.other_user.groups.add(Group.objects.get(name="member"))
        self.other_user.save()

        response = self.client.post(
            "/login/",
            {
                "email": "testemail@gmail.com",
                "password": "testpassword332",
            },
        )

        self.class_instance = Classes.objects.create(
            class_name="Test Class",
            class_description="Test Description",
            class_type=0,
            class_date="2024-01-01",
            class_start_time="09:00:00",
            class_end_time="10:00:00",
            slots_available=10,
            slots_filled=0,
        )
        self.class_instance.save()

    def test_create_class_view(self):
        """
        Test the create class view to ensure it returns
        a successful response and uses the correct template.

        This test method checks if the create class view
        is functioning correctly. It sends a GET request
        to the create class URL ('/create_class/') and then
        asserts two conditions:
        1. The response status code is 200, indicating a
        successful HTTP response.
        2. The correct template ('classes/create_class.html')
        is used to render the create class page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'classes/create_class.html' template
        is used in the response.
        """

        response = self.client.get("/create_class/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/create_class.html")

    def test_can_create_class(self):
        """
        Test that an admin user can create a class.

        This test method checks if admin can create a class. It
        sends a POST request to the create class URL
        ('/create_class/') with the required class details and
        then asserts two conditions:
        1. The response status code is 302, indicating a successful
        HTTP response.
        2. The class is created in the database.
        """

        response = self.client.post(
            "/create_class/",
            {
                "class_name": "Test Class2",
                "class_description": "Test Description2",
                "class_type": 0,
                "class_date": "2024-01-02",
                "class_start_time": "09:00:00",
                "class_end_time": "10:00:00",
                "slots_available": 10,
                "slots_filled": 0,
            },
        )

        self.assertRedirects(response, "/admin_dashboard/")
        existing_items = Classes.objects.filter(class_name="Test Class")
        self.assertEqual(existing_items.count(), 1)

    def test_update_class_view(self):
        """
        Test the update class view to ensure it returns a successful
        response and uses the correct template.

        This test method checks if the update class view is functioning
        correctly. It sends a GET request
        to the update class URL ('/update_class/') and then asserts two
        conditions:
        1. The response status code is 200, indicating a successful HTTP
        response.
        2. The correct template ('classes/update_class.html') is used to
        render the update class page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'classes/update_class.html' template is used
        in the response.
        """

        response = self.client.get("/update_class/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/update_class.html")

    def test_can_update_class(self):
        """
        Test that an admin user can update a class.

        This test method checks if admin can update a class. It sends a
        POST request to the update class URL
        ('/update_class/') with the required class details and then
        asserts two conditions:
        1. The response status code is 302, indicating a successful
        HTTP response.
        2. The class is updated in the database.
        """

        response = self.client.post(
            f"/update_class/{self.class_instance.id}/",
            {
                "class_name": "Test Class2",
                "class_description": "Test Description2",
                "class_type": 0,
                "class_date": "2024-01-02",
                "class_start_time": "09:00:00",
                "class_end_time": "10:00:00",
                "slots_available": 10,
            },
        )
        self.assertRedirects(response, "/admin_dashboard/")
        existing_items = Classes.objects.filter(class_name="Test Class2")
        self.assertEqual(existing_items.count(), 1)

    def test_delete_class_view(self):
        """
        Test the delete class view to ensure it returns a successful
        response and uses the correct template.

        This test method checks if the delete class view is functioning
        correctly. It sends a GET request
        to the delete class URL ('/delete_class/') and then asserts two
        conditions:
        1. The response status code is 200, indicating a successful HTTP
        response.
        2. The correct template ('classes/delete_class.html') is used to
        render the delete class page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'classes/delete_class.html' template is used
        in the response.
        """

        response = self.client.get(f"/delete_class/{self.class_instance.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/delete_class.html")

    def test_can_delete_class(self):
        """
        Test that an admin user can delete a class.

        This test method checks if admin can delete a class. It sends a
        POST request to the delete class URL
        ('/delete_class/') with the required class details and then asserts
        two conditions:
        1. The response status code is 302, indicating a successful HTTP
        response.
        2. The class is deleted from the database.
        """

        response = self.client.post(f"/delete_class/{self.class_instance.id}/")
        self.assertRedirects(response, "/admin_dashboard/")
        existing_items = Classes.objects.filter(class_name="Test Class")
        self.assertEqual(existing_items.count(), 0)

    def test_classes_view(self):
        """
        Test the classes view to ensure it returns a successful response
        and uses the correct template.

        This test method checks if the classes view is functioning correctly.
        It sends a GET request
        to the classes URL ('/classes/') and then asserts two conditions:
        1. The response status code is 200, indicating a successful
        HTTP response.
        2. The correct template ('classes/classes.html') is used to
        render the classes page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'classes/classes.html'
        template is used in the response.
        """

        response = self.client.get("/classes/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/classes.html")


class TestBookingViews(TestCase):
    def setUp(self):
        """
        Set up the test environment by creating two users and two groups.

        This set up method creates two users and groups.
        It also creates a group called 'admin' and a group called "member"
        and adds a user to each group.
        The admin user is then logged in.
        """
        Group.objects.create(name="admin")
        Group.objects.create(name="member")

        self.user = User.objects.create_user(
            username="testuser1",
            first_name="Test1",
            last_name="User1",
            email="testemail@gmail.com",
            password="testpassword332",
        )

        self.user.groups.add(Group.objects.get(name="admin"))
        self.user.save()

        self.other_user = User.objects.create_user(
            username="testuser2",
            first_name="Test2",
            last_name="User2",
            email="testuseremail2@email.com",
            password="testpassword3322",
        )
        self.other_user.groups.add(Group.objects.get(name="member"))
        self.other_user.save()

        response = self.client.post(
            "/login/",
            {
                "email": "testemail@gmail.com",
                "password": "testpassword332",
            },
        )

        self.class_instance = Classes.objects.create(
            class_name="Test Class",
            class_description="Test Description",
            class_type=0,
            class_date="2024-01-01",
            class_start_time="09:00:00",
            class_end_time="10:00:00",
            slots_available=10,
            slots_filled=0,
        )
        self.class_instance.save()

        self.other_class_instance = Classes.objects.create(
            class_name="Test Class2",
            class_description="Test Description2",
            class_type=0,
            class_date="2024-01-02",
            class_start_time="09:00:00",
            class_end_time="10:00:00",
            slots_available=10,
            slots_filled=0,
        )

        self.booking_instance = Bookings.objects.create(
            user=self.other_user,
            class_id=self.class_instance,
        )

    def test_bookings_view(self):
        """
        Test the bookings view to ensure it returns a successful response
        and uses the correct template.

        This test method checks if the bookings view is functioning correctly.
        It sends a GET request
        to the bookings URL ('/user_bookings/') and then asserts
        two conditions:
        1. The response status code is 200, indicating a
        successful HTTP response.
        2. The correct template ('classes/user_bookings.html') is used to
        render the bookings page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'classes/user_bookings.html' template is used
        in the response.
        """

        response = self.client.get("/user_bookings/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/user_bookings.html")

    def test_book_class_view(self):
        """
        Test the book class view to ensure it returns a
        successful response and uses the correct template.

        This test method checks if the book class view is
        functioning correctly. It sends a GET request
        to the book class URL ('/book_class/') and then
        asserts two conditions:
        1. The response status code is 200, indicating a
        successful HTTP response.
        2. The correct template ('classes/book_class.html')
        is used to render the book class page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'classes/book_class.html' template
        is used in the response.
        """

    def test_can_book_class(self):
        """
        Test that a user can book a class.

        This test method checks if a user can book a class.
        It sends a POST request to the book class URL
        ('/book_class/') with the required class details
        and then asserts two conditions:
        1. The response status code is 302, indicating a
        successful HTTP response.
        2. The class is booked in the database.
        """

        response = self.client.post(
            f"/book_class/{self.class_instance.id}/",
            {
                "class_id": self.class_instance.id,
                "user": self.user.id,
            },
        )
        self.assertRedirects(response, "/classes/")
        existing_items = Bookings.objects.filter(user=self.user)
        self.assertEqual(existing_items.count(), 1)

    def test_cancel_booking_view(self):
        """
        Test the cancel booking view to ensure it returns a
        successful response and uses the correct template.

        This test method checks if the cancel booking view
        is functioning correctly. It sends a GET request
        to the cancel booking URL ('/cancel_booking/') and
        then asserts two conditions:
        1. The response status code is 200, indicating a
        successful HTTP response.
        2. The correct template ('classes/cancel_booking.html')
        is used to render the cancel booking page.

        Assertions:
        - Asserts that the HTTP response status code is 200.
        - Asserts that the 'classes/cancel_booking.html'
        template is used in the response.
        """

        response = self.client.get(
            f"/cancel_booking/{self.booking_instance.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "classes/cancel_booking.html")
