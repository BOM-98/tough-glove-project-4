"""
URL configuration for tough_glove project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from layout.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", homepage, name="homepage"),
    path("register/", register_view, name="register"),
    path("create_member/", create_member_view, name="create_member"),
    path("login/", login_view, name="login"),
    path("logout/", logout_user, name="logout"),
    path("available_classes/", available_classes_view, name="available_classes"),
    path("members/", members_view, name="members"),
    path("update_member/<str:pk>/", update_member_view, name="update_member"),
    path("delete_member/<str:pk>/", delete_member_view, name="delete_member"),
    path("admin_dashboard/", admin_dashboard_view, name="admin_dashboard"),
    path("create_class/", create_class_view, name="create_class"),
    path("update_class/<str:pk>/", update_class_view, name="update_class"),
    path("delete_class/<str:pk>/", delete_class_view, name="delete_class"),
    path("classes/", classes_view, name="classes"),
    path("book_class/<str:pk>/", book_class_view, name="book_class"),
    path("user_bookings/", user_bookings_view, name="user_bookings"),
]
