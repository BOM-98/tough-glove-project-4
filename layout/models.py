from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

# Create your models here.
STATUS = ((0, "Draft"), (1, "Publish"))
CLASSES = ((0, "Group"), (1, "Private"))

class Members(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, unique=True)
    
    class Meta:
        verbose_name_plural = 'Members'
        ordering = ['-date_joined']
        
    def __str__(self):
        return self.user.get_full_name() + " " + self.user.email

class Classes(models.Model):
    class_name = models.CharField(max_length=200)
    class_description = models.TextField()
    class_type = models.IntegerField(choices=CLASSES, default=0)
    class_date = models.DateField()
    class_start_time = models.TimeField()
    class_end_time = models.TimeField()
    slots_available = models.IntegerField()
    slots_filled = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Classes'
        ordering = ['-class_date']
        unique_together = ['class_date', 'class_start_time', 'class_end_time']
    
class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Bookings'
        ordering = ['-booking_date']
        unique_together = ['user', 'class_id']
      
@receiver(post_delete, sender=Bookings)
def decrement_slots(sender, instance, **kwargs):
    """
    Signal handler to decrement the number of filled slots and increment the 
    number of available slots for a class when a booking is deleted.

    Args:
        sender (Model): The model class that sent the signal.
        instance (Bookings): The instance of the Bookings model being deleted.
        **kwargs: Additional keyword arguments provided by the signal.

    Returns:
        None
    """
    class_instance = instance.class_id
    class_instance.slots_available += 1
    class_instance.slots_filled -= 1
    class_instance.save()