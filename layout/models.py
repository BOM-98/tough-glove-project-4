from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from cloudinary.models import CloudinaryField

# Create your models here.
STATUS = ((0, "Draft"), (1, "Publish"))
CLASSES = ((0, "Group"), (1, "Private"))


class Members(models.Model):
    """
    A Django model representing a member of the fitness center.

    This model extends Django's built-in Model class and
    is designed to store information about members of the gym.

    Attributes:
    - user (OneToOneField): A one-to-one link to Django's User model.
    This field is nullable, and the member record is deleted if the
    linked User record is deleted.
    - date_joined (DateTimeField): The date and time when the member
    joined the fitness center. This field is automatically set to the
    current date and time when a new member record is created.
    - phone_number (CharField): The member's phone number. This field
    is unique, ensuring no two members have the same phone number.

    Meta:
    - verbose_name_plural (str): The plural name for the model in the
    admin interface.
    - ordering (list): Default ordering of member records, set to
    display the most recently joined members first.

    Methods:
    - __str__(self): Returns a string representation of the member,
    combining the member's full name and email address.
    This method is useful for displaying member information in a
    readable format, especially in admin interfaces or debug outputs.
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name_plural = 'Members'
        ordering = ['-date_joined']

    def __str__(self):
        return self.user.get_full_name() + " " + self.user.email
# The above class is a model class in Python.


class Classes(models.Model):
    """
    Represents a fitness class in Tough Glove.

    This model is designed to store and manage
    information about various fitness classes offered.

    Attributes:
    - class_name (CharField): The name of the boxing class.
    - class_description (TextField): A detailed description of
    what the class entails.
    - class_type (IntegerField): The type of class, represented
    by an integer. The choices for this field are defined in the
    CLASSES constant.
    - class_date (DateField): The date on which the class is
    scheduled.
    - class_start_time (TimeField): The starting time of the
    class.
    - class_end_time (TimeField): The ending time of the class.
    - slots_available (IntegerField): The total number of slots
    available for participants to book.
    - slots_filled (IntegerField): The number of slots that have
    already been filled. Defaults to 0.

    Meta:
    - verbose_name_plural (str): A human-readable plural name
    for the class, which is used in the Django admin.
    - ordering (list): The default ordering for the queryset,
    which in this case is descending by class_date.
    - unique_together (tuple): A set of field names that,
    taken together, must be unique throughout the table.
    This ensures that no two classes
    can have the same date and start/end times.
    """
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
    """
    Represents a booking for a boxing class by a user.

    This model is used to track and manage bookings made
    by users for various boxing classes.

    Attributes:
    - user (ForeignKey): A reference to the User model,
    indicating which user has made the booking.
    - class_id (ForeignKey): A reference to the Classes model,
    indicating which class has been booked.
    - booking_date (DateTimeField): The date and time when the
    booking was made. This is automatically set to the current
    date and time when a booking instance is created.

    Meta:
    - verbose_name_plural (str): A human-readable plural name
    for the class, which is used in the Django admin.
    - ordering (list): The default ordering for the queryset,
    which in this case is descending by booking_date.
    - unique_together (tuple): A set of field names that, taken
    together, must be unique throughout the table. This ensures
    that a user cannot book the same class more than once.
    """
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
    Signal handler to decrement the number of filled slot
    and increment the
    number of available slots for a class when a booking
    is deleted.

    Args:
        sender (Model): The model class that sent the
        signal.
        instance (Bookings): The instance of the Bookings
        model being deleted.
        **kwargs: Additional keyword arguments provided
        by the signal.

    Returns:
        None
    """
    class_instance = instance.class_id
    class_instance.slots_available += 1
    class_instance.slots_filled -= 1
    class_instance.save()
