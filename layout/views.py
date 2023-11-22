# Standard library imports

# Related third-party imports
from django.db import models, IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin


# Local application/library specific imports
from .forms import *
from layout.booking_functions.availability import get_available_classes
from .decorators import unauthenticated_user, allowed_users
from .models import *


# Create your views here.
def homepage(request):
    """
    Render the homepage view.

    This view returns the homepage template for
    the website. It is a simple view that
    only renders the template without any
    additional context or processing.

    Parameters:
    request (HttpRequest): The HttpRequest
    object that represents the client's request.

    Returns:
    HttpResponse: An HttpResponse object
    that renders the 'layout/homepage.html' template.
    """

    return render(request, "layout/homepage.html")


@unauthenticated_user
def register_view(request):
    """
    Handle the user registration process.

    This view function is responsible for displaying
    the user registration form and processing
    the form data to create a new user account. It
    uses the `CreateUserForm` to validate the
    user input. If the form submission is valid, a
    new user is created, added to the 'member'
    group, and a success message is displayed. The
    user is then redirected to the login page.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: An HTTP response object that renders
    the registration form on GET requests,
    or redirects to the login page on successful
    POST requests.

    Decorators:
    - @unauthenticated_user: A decorator to restrict
    access to this view for already authenticated users.

    The function first checks if the request method
    is POST. If so, it processes the form data.
    If the form is valid, it saves the new user,
    adds them to the 'member' group, and redirects
    to the login page. If the request method is
    not POST (i.e., GET), it displays the registration
    form to the user.
    """

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            group = Group.objects.get(name="member")
            user.groups.add(group)
            messages.success(
                request, "Account created successfully for " + username)
            return redirect("login")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


@allowed_users(allowed_roles=["admin"])
def create_member_view(request):
    """
    Handle the creation of a new member account by an admin.

    This view function is used by administrators
    to create new member accounts. It displays
    the `CreateUserForm` for input and processes
    the submitted form data. If the form is valid,
    a new user account is created, the user is
    added to the 'member' group, and a success message
    is displayed. After successful account
    creation, the admin is redirected to the members page.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: An HTTP response object
    that renders the registration form on GET requests,
    or redirects to the members page on
    successful POST requests.

    Decorators:
    - @allowed_users(allowed_roles=['admin']):
    A decorator to restrict access to this view to users
    with the 'admin' role.

    The function checks if the request method
    is POST. If so, it processes the form data. If the
    form is valid, it saves the new user, adds
    them to the 'member' group, and redirects to the
    members page. If the request method is not
    POST (i.e., GET), it displays the registration form
    to the admin.
    """

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            group = Group.objects.get(name="member")
            user.groups.add(group)
            messages.success(
                request, "Account created successfully for " + username)
            return redirect("members")

    context = {"form": form}
    return render(request, "accounts/register.html", context)


@unauthenticated_user
def login_view(request):
    """
    Handle the user login process.

    This view function is responsible for authenticating
    users. It displays a login form and
    processes the submitted credentials.
    If the credentials are valid, the user
    is logged in
    and redirected to the homepage.
    Otherwise, an error message is displayed.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: An HTTP response object
    that renders the login form on GET requests,
    or processes the login on POST requests.

    Decorators:
    - @unauthenticated_user: A decorator to
    ensure that this view is only accessible to
    users who are not currently authenticated.

    The function checks if the request method
    is POST. If so, it retrieves the email and password
    from the request. It then attempts to find
    a user with the given email. If a user is found and
    the password is correct, the user is logged
    in and redirected to the homepage. If the credentials
    are incorrect, an error message is displayed.
    For GET requests, the login form is displayed.
    """

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        # Check the password if the user exists
        if user is not None and user.check_password(password):
            # Manually authenticate the user, then login
            login(request, user)
            return redirect("homepage")
        else:
            messages.info(request, "Email or password is incorrect")

    context = {}
    return render(request, "accounts/login.html", context)


def logout_user(request):
    """
    Log out the current user and redirect to the homepage.

    This view function is responsible for logging
    out the currently authenticated user.
    It calls Django's `logout` function, which
    handles the process of invalidating the
    user's session. After logging out, the user
    is redirected to the homepage.

    Args:
    - request (HttpRequest): The HTTP request
    object.

    Returns:
    - HttpResponseRedirect: A redirect to the
    homepage URL.

    The function does not require any arguments
    from the request object, nor does it
    process any data. It simply logs out the user
    and redirects to the homepage, making
    it a straightforward and concise view for
    handling user logout.
    """
    logout(request)
    return redirect("homepage")


@login_required(login_url="login")
@allowed_users(allowed_roles=["member", "admin"])
def available_classes_view(request):
    """
    Display the available classes to the user.

    This view is accessible only to authenticated
    users with 'member' or 'admin' roles.
    It retrieves a list of available classes and
    renders them using the
    'layout/available_classes.html' template. The
    view is decorated with `login_required`
    and `allowed_users` to enforce access control.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: An HTTP response object with
    the rendered template.

    The function calls `get_available_classes`,
    which is responsible for fetching the
    available classes from the database. It then
    passes these classes to the template
    context. This view is crucial for users to
    browse and select classes they might be
    interested in attending.
    """
    available_classes = get_available_classes()
    return render(
        request,
        "layout/available_classes.html",
        {"available_classes": available_classes},
    )


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def members_view(request):
    """
    Display the members page to admin users.

    This view function is responsible for rendering
    the members page. It is accessible only to users
    with 'admin' role.
    The function performs the following operations:
    1. Retrieves all member records from the Members model.
    2. Fetches all user records from the User model.
    3. Counts the total number of users.
    4. Passes the members, users, and user count
    to the 'accounts/members.html' template.

    Parameters:
    - request: HttpRequest object containing metadata
    about the request.

    Returns:
    - HttpResponse object with the rendered
    'accounts/members.html' template.

    The view is decorated with @login_required and
    @allowed_users decorators to ensure that only
    authenticated users with
    'admin' role can access this page. If a non-authenticated
    user attempts to access this page, they will be redirected
    to the 'login' page. The view provides a comprehensive
    overview of members and users, useful for administrative purposes.
    """
    members = Members.objects.all()
    users = User.objects.all()
    user_count = User.objects.count()
    context = {"members": members, "users": users, "user_count": user_count}
    return render(request, "accounts/members.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin", "member"])
def profile_view(request):
    """
    Render the profile page for logged-in users.

    This view function is designed to display the profile
    page for authenticated users with either 'admin' or 'member' roles.
    It performs the following operations:
    1. Retrieves the current logged-in user's information.
    2. Fetches all member records from the Members model.
    3. Retrieves all bookings made by the current user.
    4. Extracts the classes associated with these bookings.
    5. Counts the total number of bookings made by the user.
    6. Passes the user's bookings, booking count, user
    information, associated classes, and all members to
    the 'accounts/profile.html' template.

    Parameters:
    - request: HttpRequest object containing metadata
    about the request.

    Returns:
    - HttpResponse object with the rendered
    'accounts/profile.html' template.

    The view is decorated with @login_required and
    @allowed_users decorators to ensure that only authenticated users with
    'admin' or 'member' roles can access this page.
    If a non-authenticated user attempts to access this page, they will be
    redirected to the 'login' page. This view provides
    a personalized user experience by displaying relevant user-specific
    information such as their bookings and classes.
    """
    user = request.user
    members = Members.objects.all()
    bookings = user.bookings_set.all()
    classes = [booking.class_id for booking in bookings]
    bookings_count = bookings.count()
    context = {
        "bookings": bookings,
        "bookings_count": bookings_count,
        "user": user,
        "classes": classes,
        "members": members,
    }
    return render(request, "accounts/profile.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["member", "admin"])
def update_member_view(request, pk):
    """
    Handle the request to update a member's profile.

    This view function is responsible for updating the
    profile of a member. It is accessible only to authenticated users
    with 'member' or 'admin' roles. The function performs
    several key operations:
    1. Retrieves the user object based on the provided
    primary key (pk).
    2. Initializes the UpdateUserForm with the retrieved
    user instance.
    3. Checks if the current user is authorized to update
    the profile. Unauthorized attempts result in an error
    message and redirection to the profile page.
    4. Processes the POST request to update the user's
    information if the form is valid.
    5. Redirects to the profile page upon successful
    update, displaying a success message.
    6. Renders the 'accounts/update_member.html'
    template with the form and user context if the request
    is not a POST request.

    Parameters:
    - request: HttpRequest object containing metadata
    about the request.
    - pk: Primary key of the user to be updated.

    Returns:
    - HttpResponse object with the rendered 'accounts/update_member.html'
    template or a redirect to the profile page.

    The view is decorated with @login_required and @allowed_users
    decorators to ensure that only authenticated users with
    the required roles can access this functionality.
    It provides a secure and user-friendly interface for members to update
    their profiles.
    """
    user = get_object_or_404(User, id=pk)
    form = UpdateUserForm(instance=user)
    is_admin = request.user.groups.filter(name="admin").exists()
    if not (is_admin or request.user.id == user.id):
        messages.error(
            request, "Error, you are unauthorised to edit this account.")
        return redirect("profile")
    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "This member has been updated successfully!")
            return redirect("profile")
    context = {"form": form, "user": user}
    return render(request, "accounts/update_member.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def delete_member_view(request, pk):
    """
    Handle the request to delete a member's profile.

    This view function is responsible for deleting a
    member's profile. It is accessible only to authenticated users
    with the 'admin' role. The function performs several
    key operations:
    1. Retrieves the user object based on the provided
    primary key (pk) or raises a 404 error if not found.
    2. Checks if the request method is POST, indicating
    a confirmation to delete.
    3. Deletes the user and displays a success message
    upon deletion.
    4. Redirects to the 'members' view after successful
    deletion.
    5. Renders the 'accounts/delete_member.html'
    template with the user context if the request is not a POST request.

    Parameters:
    - request: HttpRequest object containing metadata
    about the request.
    - pk: Primary key of the user to be deleted.

    Returns:
    - HttpResponse object with the rendered 'accounts/delete_member.html'
    template or a redirect to the 'members' view.

    The view is decorated with @login_required and @allowed_users
    decorators to ensure that only authenticated users with
    the 'admin' role can access this functionality. It provides
    a secure and controlled way for administrators to manage
    user profiles by deleting them when necessary.
    """
    user = get_object_or_404(User, id=pk)
    if request.method == "POST":
        user.delete()
        messages.success(
            request, "This member has been deleted!")
        return redirect("members")
    context = {"user": user}
    return render(
        request, "accounts/delete_member.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def admin_dashboard_view(request):
    """
    Render the admin dashboard view with relevant data.

    This view function is designed for administrators to provide
    an overview of the platform's key metrics. It is
    accessible only to authenticated users with the 'admin' role.
    The function performs several key operations:
    1. Retrieves all users, classes, and members from the database.
    2. Counts the total number of users, classes, personal
    training classes, and group classes.
    3. Fetches available classes using the `get_available_classes`
    function.
    4. Renders the 'layout/admin_dashboard.html' template with
    the context containing all the retrieved data.

    Parameters:
    - request: HttpRequest object containing metadata about the request.

    Returns:
    - HttpResponse object with the rendered 'layout/admin_dashboard.html'
    template.

    The view is decorated with @login_required and @allowed_users
    decorators to ensure that only authenticated users with
    the 'admin' role can access this functionality. It provides
    a comprehensive dashboard for administrators to monitor
    and manage the platform effectively, offering insights into
    user engagement, class offerings, and overall platform
    activity.
    """
    users = User.objects.all()
    classes = Classes.objects.all()
    members = Members.objects.all()
    user_count = User.objects.count()
    classes_count = Classes.objects.count()
    pt_classes_count = Classes.objects.filter(class_type=1).count()
    group_classes_count = Classes.objects.filter(class_type=0).count()
    available_classes = get_available_classes()
    context = {
        "users": users,
        "classes": classes,
        "members": members,
        "user_count": user_count,
        "classes_count": classes_count,
        "pt_classes_count": pt_classes_count,
        "group_classes_count": group_classes_count,
        "available_classes": available_classes,
    }
    return render(request, "layout/admin_dashboard.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def create_class_view(request):
    """
    Render the view for creating a new class and handle the class
    creation process.

    This view function is accessible only to authenticated users
    with the 'admin' role. It serves two primary purposes:
    1. Display the class creation form (CreateClassForm)
    when accessed via a GET request.
    2. Handle the submission of the class creation form
    when accessed via a POST request.

    If the form is submitted and valid, a new class is saved
    to the database, and the user is redirected to the
    admin dashboard with a success message. If the form is
    not valid, the form with errors is rendered back to the user.

    Parameters:
    - request: HttpRequest object containing metadata about the request.

    Returns:
    - HttpResponse object with the rendered
    'classes/create_class.html' template.

    The view is decorated with @login_required and @allowed_users
    decorators to ensure that only authenticated users with
    the 'admin' role can access and perform class creation.
    This function is crucial for the dynamic management of class
    offerings on the platform, allowing administrators to
    add new classes as per the requirements.

    The context passed to the template includes the class
    creation form and a list of all existing classes, providing
    administrators with a comprehensive view for managing
    classes.
    """
    if request.method == "POST":
        form = CreateClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "class created successfully!")
            return redirect("admin_dashboard")
    classes = Classes.objects.all()
    context = {"classes": classes, "form": CreateClassForm()}
    return render(request, "classes/create_class.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def update_class_view(request, pk):
    """
    Render the view for updating an existing class and handle
    the class update process.

    This view function is accessible only to authenticated
    users with the 'admin' role. It serves two primary purposes:
    1. Display the class update form (UpdateClassForm) pre-filled
    with the existing class data when accessed via a GET request.
    2. Handle the submission of the class update form when accessed
    via a POST request.

    The function retrieves the class to be updated using the
    primary key (pk) provided in the URL. If the form is submitted
    and valid, the changes are saved to the database, and
    the user is redirected to the admin dashboard with a success message.
    If the form is not valid, the form with errors is
    rendered back to the user.

    Parameters:
    - request: HttpRequest object containing metadata about the request.
    - pk: Primary key of the class to be updated.

    Returns:
    - HttpResponse object with the rendered
    'classes/update_class.html' template.

    The view is decorated with @login_required and
    @allowed_users decorators to ensure that only authenticated users with
    the 'admin' role can access and perform class updates.
    This function is crucial for maintaining and modifying the
    details of existing classes, allowing administrators
    to update class information as needed.

    The context passed to the template includes the
    class update form and the class object being updated, providing
    administrators with a user-friendly interface for
    editing class details.
    """
    update_class = Classes.objects.get(id=pk)
    form = UpdateClassForm(instance=update_class)
    if request.method == "POST":
        form = UpdateClassForm(request.POST, instance=update_class)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your class has been updated successfully!")
            return redirect("admin_dashboard")
    context = {"class": update_class, "form": form}
    return render(request, "classes/update_class.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def delete_class_view(request, pk):
    """
    Render the view for deleting an existing class and
    handle the class deletion process.

    This view function is accessible only to authenticated
    users with the 'admin' role. It serves two primary purposes:
    1. Display a confirmation page for class deletion
    when accessed via a GET request.
    2. Handle the actual deletion of the class when
    accessed via a POST request.

    The function retrieves the class to be deleted using
    the primary key (pk) provided in the URL. If the deletion is
    confirmed through a POST request, the class is deleted
    from the database, and the user is redirected to the admin
    dashboard with a success message.

    Parameters:
    - request: HttpRequest object containing metadata
    about the request.
    - pk: Primary key of the class to be deleted.

    Returns:
    - HttpResponse object with the rendered
    'classes/delete_class.html' template.

    The view is decorated with @login_required and
    @allowed_users decorators to ensure that only
    authenticated users with
    the 'admin' role can access and perform class
    deletions. This function plays a critical role in managing the class
    offerings, allowing administrators to remove
    classes that are no longer needed or relevant.

    The context passed to the template includes the
    class object being deleted, providing administrators with a clear
    and concise interface for confirming the deletion
    of class details.
    """
    delete_class = Classes.objects.get(id=pk)
    if request.method == "POST":
        delete_class.delete()
        messages.success(request, "Your class has been deleted successfully!")
        return redirect("admin_dashboard")
    context = {"class": delete_class}
    return render(request, "classes/delete_class.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["member", "admin"])
def classes_view(request):
    """
    Render the view for displaying all classes,
    including available and total class counts.

    This view function is accessible to authenticated
    users with either 'member' or 'admin' roles. It serves to present
    a comprehensive overview of all classes offered,
    along with additional details like the total number
    of classes and
    the number of available classes.

    The function fetches all class instances from the
    database and calculates the total count of classes. It also
    retrieves the list of available classes through the
    `get_available_classes` function. Additionally, it fetches all
    user instances for potential use in the template.

    Parameters:
    - request: HttpRequest object containing metadata about the request.

    Returns:
    - HttpResponse object with the rendered 'classes/classes.html' template.

    The view is decorated with @login_required and
    @allowed_users decorators to ensure that only authenticated users with
    the appropriate roles can access this view. This
    function is crucial for providing users with a clear
    and detailed
    view of the classes, enabling them to make informed
    decisions about class participation or administration.

    The context passed to the template includes the list
    of all classes, the total count of classes, the list of
    available classes, and all user instances. This rich
    context allows for a dynamic and informative user interface,
    catering to both regular members and administrators.
    """
    classes = Classes.objects.all()
    classes_count = Classes.objects.count()
    available_classes = get_available_classes()
    users = User.objects.all()
    context = {
        "classes": classes,
        "classes_count": classes_count,
        "available_classes": available_classes,
        "users": users,
    }
    return render(request, "classes/classes.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["member", "admin"])
def user_bookings_view(request):
    """
    Render the view for a user's bookings, including details
    of each booking and the total count.

    This view function is accessible to authenticated users
    with either 'member' or 'admin' roles. It is designed to
    provide users with a personalized overview of their bookings,
    including details of the classes they have booked and
    the total number of bookings they have made.

    The function retrieves the current user from the request,
    fetches all bookings related to this user, and calculates
    the total number of bookings. It also compiles a list of
    classes associated with these bookings for display in the
    template.

    Parameters:
    - request: HttpRequest object containing metadata about
    the request.

    Returns:
    - HttpResponse object with the rendered
    'classes/user_bookings.html' template.

    The view is decorated with @login_required and @allowed_users
    decorators to ensure that only authenticated users with
    the appropriate roles can access this view. This function
    plays a key role in enhancing user experience by providing
    a tailored view of their bookings, allowing them to easily
    manage and review their scheduled classes.

    The context passed to the template includes the list of the
    user's bookings, the total count of these bookings, the
    user instance, and the list of classes associated with the
    bookings. This comprehensive context facilitates a
    user-centric interface, enabling users to have a clear and
    detailed view of their scheduled activities.
    """
    user = request.user
    bookings = user.bookings_set.all()
    classes = [booking.class_id for booking in bookings]
    bookings_count = bookings.count()
    context = {
        "bookings": bookings,
        "bookings_count": bookings_count,
        "user": user,
        "classes": classes,
    }
    return render(request, "classes/user_bookings.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["member", "admin"])
def book_class_view(request, pk):
    """
    Handle the booking of a class by a user, including form
    validation and updating class availability.

    This view function allows authenticated users with 'member'
    or 'admin' roles to book a class. It handles both the
    display of the booking form and the processing of the form
    submission. The function ensures that the booking
    process is robust, handling scenarios such as fully booked
    classes and duplicate bookings.

    Parameters:
    - request: HttpRequest object containing metadata about
    the request.
    - pk: Primary key of the class to be booked.

    Returns:
    - HttpResponse object with the rendered 'classes/book_class.html'
    template.

    The function first retrieves the class instance using the
    provided primary key. If the request method is POST, it
    processes the submitted form data. The form is validated
    to ensure that the booking details are correct. If the
    form is valid, a new booking is created and linked to the
    user and the class. The class's available slots are
    updated accordingly. If the class is fully booked or if
    the user has already booked the class, appropriate error
    messages are added to the form.

    If the request method is not POST, the function initializes
    a pre-populated form with the class and user details.

    The view is decorated with @login_required and @allowed_users
    decorators to ensure that only authenticated users
    with the appropriate roles can access this view. This
    function is crucial for managing class bookings, ensuring
    that users can easily book classes while maintaining
    the integrity of class availability and preventing duplicate
    bookings.

    The context passed to the template includes the booking
    form and the class instance, providing the necessary
    information for users to make a booking and for the
    template to display the relevant class details.
    """
    class_instance = Classes.objects.get(id=pk)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.class_id = class_instance
            class_instance.slots_filled += 1
            class_instance.slots_available -= 1
            if "cancel" in request.POST:
                return redirect("classes")
            else:
                if class_instance.slots_available == 0:
                    form.add_error(None, "This class is now fully booked")
                try:
                    booking.save()
                    class_instance.save()
                    messages.success(
                        request, "Your class has been booked successfully!"
                    )
                    return redirect("classes")
                except IntegrityError:
                    form.add_error(None, "You have already booked this class")

    else:
        initial_data = {"class_id": class_instance.id, "user": request.user.id}
        form = BookingForm(initial_data)

    context = {
        "form": form,
        "class": class_instance,
    }
    return render(request, "classes/book_class.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["member", "admin"])
def cancel_booking_view(request, pk):
    """
    Handle the cancellation of a user's class booking.

    This view function allows authenticated users with 'member'
    or 'admin' roles to cancel a class booking. It
    facilitates the process of canceling a booking by handling
    the request to delete a specific booking instance
    identified by its primary key.

    Parameters:
    - request: HttpRequest object containing metadata about
    the request.
    - pk: Primary key of the booking to be canceled.

    Returns:
    - HttpResponse object with the rendered
    'classes/cancel_booking.html' template.
    """
    booking_instance = Bookings.objects.get(id=pk)
    if request.method == "POST":
        if "cancel" in request.POST:
            return redirect("user_bookings")
        else:
            booking_instance.delete()
            messages.success(request, "Your booking has been canceled!")
            return redirect("user_bookings")
    context = {"booking": booking_instance}
    return render(request, "classes/cancel_booking.html", context)


def get_classes(request):
    """
    Retrieve all class instances from the database and
    return them in a JSON format.

    Parameters:
    - request: HttpRequest object containing metadata
    about the request.

    The function performs the following operations:
    1. Queries the Classes model to retrieve all
    class instances.
    2. Iterates over each class instance, formatting
    the relevant information (class name, start date and
    time, end date and time) into a dictionary.
    3. Compiles these dictionaries into a list.

    This list is used for displaying the classes in
    the calendar view.
    """
    classes = Classes.objects.all()
    class_list = [
        {
            "title": class_instance.class_name,
            "start": f"{
                class_instance.class_date} {class_instance.class_start_time}",
            "end": f"{
                class_instance.class_date} {class_instance.class_end_time}",
        }
        for class_instance in classes
    ]
    return JsonResponse(class_list, safe=False)
