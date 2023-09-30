from django.contrib import admin
from .models import Users, Classes, Bookings, BlogPosts

admin.site.register(Users)
admin.site.register(Classes)
admin.site.register(Bookings)
admin.site.register(BlogPosts)

# Register your models here.
