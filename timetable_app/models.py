from django.db import models

# Teacher Model
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    availability = models.JSONField()  # Available hours for each day
    subjects = models.ManyToManyField('Subject')  # Subjects a teacher can teach

    def __str__(self):
        return self.name

# Subject Model
class Subject(models.Model):
    name = models.CharField(max_length=100)
    required_periods_per_week = models.IntegerField(default=1)  # Required lessons per week
    is_double_period = models.BooleanField(default=False)  # Whether the subject requires double periods

    def __str__(self):
        return self.name

# Room Model
class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()  # Capacity of the room

    def __str__(self):
        return self.name

# StudentGroup Model
class StudentGroup(models.Model):
    name = models.CharField(max_length=100)
    students = models.IntegerField()

    def __str__(self):
        return self.name

# TimeSlot Model
class TimeSlot(models.Model):
    day_of_week = models.CharField(max_length=20)
    period_number = models.IntegerField()  # 1-8 for KS3, 1-9 for KS4

    def __str__(self):
        return f"{self.day_of_week} - Period {self.period_number}"

# SpecialPeriod Model (e.g., TP3, Clubs)
class SpecialPeriod(models.Model):
    name = models.CharField(max_length=100)
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
    identification_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.identification_number
