from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages


def unauthenticated_user(view_func):
    """
    Decorator for views that redirects authenticated users to the classes page.

    This decorator is used in Django views to prevent authenticated
    (logged-in) users from accessing
    certain pages that are intended only for
    unauthenticated (not logged-in) users.

    Parameters:
    - view_func (function): The view function that should
    be accessible only to unauthenticated users.

    Returns:
    - A redirect to a predefined page ('classes') if the user is authenticated.
    - The original view function if the user is not authenticated.
    """

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("classes")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    """
    Decorator for views that checks whether the user belongs to
    a specified group, denying access if not.

    This decorator function is used to restrict access to certain
    views based on the user's group membership
    in Django.

    Parameters:
    - allowed_roles (list): A list of strings representing the group
    names that are allowed to access the
    decorated view. Default is an empty list, which means no group is allowed.

    Returns:
    - The original view function if the user is in an allowed group.
    - HttpResponse with a message "You are not authorized to view this
    page" if the user is not in an
    allowed group.
    """

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request, "You are not authorized to view this page")
                return redirect("homepage")

        return wrapper_func

    return decorator
