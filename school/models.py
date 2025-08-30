from django.db import models
from django.contrib.auth.models import User

# Classes list for StudentExtra model
classes = [
    ('one', 'one'), ('two', 'two'), ('three', 'three'),
    ('four', 'four'), ('five', 'five'), ('six', 'six'),
    ('seven', 'seven'), ('eight', 'eight'), ('nine', 'nine'), ('ten', 'ten')
]


# Teacher Extra Information Model
class TeacherExtra(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.PositiveIntegerField(null=True, blank=True)
    date_of_application = models.DateField(verbose_name="Date of Application")
    mobile = models.CharField(max_length=11)
    course_of_study = models.CharField(max_length=50)
    address = models.TextField(null=True, blank=True)
    salary = models.PositiveIntegerField(default=0)  # Added for admin dashboard
    status = models.BooleanField(default=False) # Ensure default is False
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of Birth")
    
    def __str__(self):
        return self.username.first_name

    @property
    def get_id(self):
        return self.username.id

    @property
    def get_name(self):
        return self.username.first_name + " " + self.username.last_name


# Student Extra Information Model
class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll = models.CharField(max_length=20, unique=True, null=True, blank=True)  # ✅ new field
    cl = models.CharField("Class", max_length=40, choices=classes, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField("Date of Birth", null=True, blank=True)
    state_of_origin = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    fee = models.FloatField(default=0.0) 
    gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female'),('Other','Other')], null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)


    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name


# Attendance Model
STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent')]

class Attendance(models.Model):
    student = models.ForeignKey(StudentExtra, on_delete=models.CASCADE)
    date = models.DateField()
    cl = models.CharField(max_length=10)
    present_status = models.CharField(max_length=10, choices=STATUS_CHOICES)


# Notice Model
class Notice(models.Model):
    date = models.DateField(auto_now=True)
    by = models.CharField(max_length=20, null=True, default='school')
    message = models.CharField(max_length=500)


class AdminExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)  # False = not approved, True = approved

    def __str__(self):
        return self.user.username

