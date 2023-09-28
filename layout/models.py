from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
STATUS = ((0, "Draft"), (1, "Publish"))
CLASSES = ((0, "Group"), (1, "Private"))

class Users(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=200, unique=True)
    
    class Meta:
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
        
    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.email

class Classes(models.Model):
    class_name = models.CharField(max_length=200)
    class_description = models.TextField()
    class_type = models.IntegerField(choices=CLASSES, default=0)
    class_date = models.DateTimeField()
    class_start_time = models.TimeField()
    class_end_time = models.TimeField()
    slots_available = models.IntegerField()
    slots_filled = models.IntegerField()
    
    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ['-class_date']
        unique_together = ['class_date', 'class_start_time', 'class_end_time']
        
    def __str__(self):
        return self.class_name + " " + self.class_type + " " + self.class_date
    
class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Bookings'
        ordering = ['-booking_date']
        
    def __str__(self):
        return self.user + " " + self.class_id + " " + self.booking_date

class BlogPosts(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=200)
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    
    class Meta:
        verbose_name_plural = 'BlogPosts'
        ordering = ['-created_on']
        
    def __str__(self):
        return self.title + " " + self.author + " " + self.post_date
    
class Comments(models.Model):
    post = models.ForeignKey(BlogPosts, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)
    content = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Comments'
        ordering = ['-comment_date']
        
    def __str__(self):
        return self.post + " " + self.author + " " + self.comment_date