from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.conf import settings
from PIL import Image

class Teacher(models.Model):
    name = models.CharField(max_length=40)
    availability = models.JSONField()  # Available hours for each day
    subjects = models.ManyToManyField('Subject')  # Subjects a teacher can teach

    def __str__(self):
        return self.name

# Subject Model
class Subject(models.Model):
    name = models.CharField(max_length=20)
    required_periods_per_week = models.IntegerField(default=1)  # Required lessons per week
    is_double_period = models.BooleanField(default=False)  # Whether the subject requires double periods

    def __str__(self):
        return self.name

# Room Model
class Room(models.Model):
    name = models.CharField(max_length=10)
    capacity = models.IntegerField()  # Capacity of the room

    def __str__(self):
        return self.name

# StudentGroup Model
class StudentGroup(models.Model):
    name = models.CharField(max_length=10)
    students = models.IntegerField()

    def __str__(self):
        return self.name

# TimeSlot Model
class TimeSlot(models.Model):
    day_of_week = models.CharField(max_length=10)
    period_number = models.IntegerField()  # 1-8 for KS3, 1-9 for KS4

    def __str__(self):
        return f"{self.day_of_week} - Period {self.period_number}"

# SpecialPeriod Model (e.g., TP3, Clubs)
class SpecialPeriod(models.Model):
    name = models.CharField(max_length=30)
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.JSONField()  # Days on which the special period occurs

    def __str__(self):
        return self.name

# TimetableEntry Model
class TimetableEntry(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student_group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    special_period = models.ForeignKey(SpecialPeriod, on_delete=models.SET_NULL, null=True, blank=True)
    is_double_period = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} with {self.teacher} in {self.room} at {self.time_slot}"





class IdentificationNumber(models.Model):
    # Define role choices
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    
    number = models.CharField(max_length=20, unique=True)  # Identification number
    is_used = models.BooleanField(default=False)  # Track usage of the identification number
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, blank=True, null=True)  # Role with choices

    def __str__(self):
        return self.number



# Custom manager for CustomUser
class CustomUserManager(BaseUserManager):
    """
    Custom manager for CustomUser.
    """

    def create_user(self, identification_number, email, password=None, **extra_fields):
        """
        Create and return a regular user with an identification number.
        """
        if not identification_number:
            raise ValueError("The Identification Number field must be set")
        if not email:
            raise ValueError("The Email field must be set")

        # Normalize email to ensure it's in proper format
        email = self.normalize_email(email)

        # Create the user instance
        user = self.model(
            identification_number=identification_number,
            email=email,
            **extra_fields
        )
        user.set_password(password)  # Set the password (hashed)
        user.save(using=self._db)  # Save to the database
        return user

    def create_superuser(self, identification_number, email, password=None, **extra_fields):
        """
        Create and return a superuser with an identification number.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Ensure superuser-specific fields are set
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        # Call the create_user method to handle common logic
        return self.create_user(identification_number, email, password, **extra_fields)


# Custom User model with identification_number
class CustomUser(AbstractUser):
    """
    Custom User model with identification_number as the username.
    """
    username =  None
    phone = models.CharField(max_length=50, blank=True, null=True)  # Optional phone number
    address = models.CharField(max_length=100, blank=True, null=True)  # Optional address
    identification_number = models.CharField(max_length=20, blank=False, null=False) 
    role = models.CharField(max_length=30, blank=False, null=False) 
    picture = models.ImageField(upload_to='profile_pictures/%y/%m/%d/', default='default.png', null=True)

    USERNAME_FIELD = 'identification_number'  # Use identification_number as the USERNAME_FIELD
    REQUIRED_FIELDS = ['email']  # Email is required for user creation

    objects = CustomUserManager()  # Custom manager

    def __str__(self):
        return self.identification_number
    
    @property
    def get_full_name(self):
        full_name = self.first_name
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return '{} ({})'.format(self.username, self.get_full_name)
    
    # @property
    # def get_full_name_slice(self):
    #     full_name_slice = self.username
    #     if self.first_name and self.last_name:
    #         full_name_slice = self.first_name + " " + self.last_name[0] + "."
    #     return full_name_slice

    # @property
    # def get_user_role(self):
    #     if self.is_superuser:
    #         return "Admin"
    #     elif self.is_student:
    #         return "Student"
    #     elif self.is_lecturer:
    #         return "Staff"
    #     elif self.is_parent:
    #         return "Parent"

    def get_picture(self):
        try:
            return self.picture.url
        except:
            no_picture = settings.MEDIA_URL + 'default.png'
            return no_picture

    # def get_absolute_url(self):
    #     return reverse('profile_single', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.picture.url != settings.MEDIA_URL + 'default.png':
            self.picture.delete()
        super().delete(*args, **kwargs)
