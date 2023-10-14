from django.contrib import admin
from .models import Members, Classes, Bookings, BlogPosts, Comments



# Register your models here.
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'updated_on', 'category']
        
admin.site.register(Members)
admin.site.register(Classes)
admin.site.register(Bookings)
admin.site.register(BlogPosts)
admin.site.register(Comments)