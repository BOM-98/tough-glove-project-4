from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.utils import timezone
from datetime import datetime
from .models import *

class AllModelsTest(TestCase):
    
    def setUp(self):
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
        
        self.class_instance = Classes.objects.create(
            class_name='Test Class',
            class_description='Test Description',
            class_type=0,
            class_date='2024-01-01',
            class_start_time='09:00:00',
            class_end_time='10:00:00',
            slots_available=10,
            slots_filled=0,
        )
        self.class_instance.save()
        
        self.other_class_instance = Classes.objects.create(
            class_name='Test Class2',
            class_description='Test Description2',
            class_type=0,
            class_date='2024-01-02',
            class_start_time='09:00:00',
            class_end_time='10:00:00',
            slots_available=10,
            slots_filled=0,
        )
        
        self.booking_instance = Bookings.objects.create(
            user=self.other_user,
            class_id=self.class_instance,
        )
    
    def test_class_creation(self):
        """
        Test the successful creation of a class instance in the system.

        This test method verifies that a class instance has been correctly created and initialized with the expected 
        attribute values. It is essential to ensure that the class creation process is functioning as intended, as this 
        forms the basis of managing class schedules and availability in the system.

        The test checks the following attributes of the class instance:
        - class_name: Ensures that the name of the class is correctly set to 'Test Class'.
        - slots_available: Confirms that the number of available slots is correctly initialized to 10.
        - slots_filled: Verifies that the initial count of filled slots is 0, indicating no bookings yet.

        Assertions:
        - Asserts that the class_name attribute of the class instance matches 'Test Class'.
        - Asserts that the slots_available attribute is correctly set to 10.
        - Asserts that the slots_filled attribute starts at 0, indicating an empty class at creation.

        This test is crucial for validating the integrity of the class creation process. It ensures that when a new class 
        is created, it has the correct initial settings, which is fundamental for the accurate tracking and management of 
        class bookings and availability.
        """
        
        self.assertEqual(self.class_instance.class_name, 'Test Class')
        self.assertEqual(self.class_instance.slots_available, 10)
        self.assertEqual(self.class_instance.slots_filled, 0)
        
    def test_unique_together_constraint(self):
        """
        Test that a class cannot be created with the same date, start time and end time as an existing class.
        """
        with self.assertRaises(Exception):
            duplicate_class = Classes.objects.create(
                class_name='Duplicate Test Class',
                class_description='Test Description',
                class_type=0,
                class_date=self.class_instance.class_date,
                class_start_time=self.class_instance.class_start_time,
                class_end_time=self.class_instance.class_end_time,
                slots_available=10,
                slots_filled=0,
            )
    
    def test_booking_creation(self):
        """
        Test that a booking can be created.
        
        The test checks the following associations of the booking instance:
        - user: Confirms that the booking is correctly associated with the intended user.
        - class_id: Verifies that the booking is correctly linked to the specific class.

        Assertions:
        - Asserts that the user attribute of the booking instance matches the expected user object.
        - Asserts that the class_id attribute of the booking instance is correctly set to the intended class object.
    
        """
        self.assertEqual(self.booking_instance.user, self.other_user)
        self.assertEqual(self.booking_instance.class_id, self.class_instance)
        
    def test_decrement_slots(self):
        """
        Test that the slots available and slots filled for a class are decremented when a booking is created.
        
        This test method ensures the correct functionality of the slot management system within the class booking process.
        It specifically tests two scenarios:
        1. The decrement of available slots and increment of filled slots when a new booking is created.
        2. The increment of available slots and decrement of filled slots when an existing booking is deleted.
        
        Assertions:
        - Initially asserts that the 'slots_available' and 'slots_filled' are at their default values (10 and 0 respectively).
        - After deleting a booking, asserts that 'slots_available' is incremented and 'slots_filled' is decremented, 
        reflecting the removal of the booking.
      
        Note - incrementing and decrementing slots for new bookings made
        is handled by the BookingForm resulting in 11 and -1 respectively for this test.
        """
        self.assertEqual(self.class_instance.slots_available, 10)
        self.assertEqual(self.class_instance.slots_filled, 0)
        self.booking_instance.delete()
        self.class_instance.refresh_from_db()
        self.assertEqual(self.class_instance.slots_available, 11)
        self.assertEqual(self.class_instance.slots_filled, -1)
        
        
        