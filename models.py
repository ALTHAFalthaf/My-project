from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib import admin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None,dob=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, role=role,dob=dob, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, role='Admin',dob=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, role=role,dob=dob, **extra_fields)  
    

class CustomUser(AbstractUser):
    ADMIN = 'Admin'
    CHILD = 'Child'
    DOCTOR = 'Doctor'
    HEALTHCARE_PROVIDER = 'HealthcareProvider'  # New role for healthcare providers
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CHILD, 'Child'),
        (DOCTOR, 'Doctor'),
        (HEALTHCARE_PROVIDER, 'HealthcareProvider'),  # Add Healthcare Provider to role choices
    ]


    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
    )

    # Fields for custom user roles
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=CHILD)  # Default role for regular users
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.ForeignKey('HealthcareProvider', on_delete=models.SET_NULL, null=True, blank=True)
    forget_password_token = models.UUIDField(null=True, blank=True) #forgetpass
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    objects = CustomUserManager()
    username = models.CharField(max_length=150, unique=False)
    # Define boolean fields for specific roles
    is_child = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=True)
    is_healthcare_provider = models.BooleanField(default=True)  # New field to indicate healthcare provider role
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email 





class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    specialty = models.CharField(max_length=100, null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    certification = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(upload_to='doctor/resume/', null=True, blank=True)
    license_copy = models.FileField(upload_to='doctor/license_copy/', null=True, blank=True)
    photo = models.ImageField(upload_to='doctor/photo/', null=True, blank=True)
    approved = models.BooleanField(default=False)  # You can set the default value as needed


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

 

class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_appointments',default=1)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments', default=1)  # Replace '1' with the default doctor's ID
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.doctor.first_name} {self.doctor.last_name} on {self.appointment_date}"

class HealthcareProvider(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='healthcare_provider_profile', null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone= models.CharField(max_length=15, blank=True, null=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    certification = models.CharField(max_length=100, null=True, blank=True)
    resume = models.FileField(upload_to='provider/resume/', null=True, blank=True)
    license_copy = models.FileField(upload_to='provider/license_copy/', null=True, blank=True)
    photo = models.ImageField(upload_to='provider/photo/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    # Add more fields as needed
   
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class BirthDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_details',default=1)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    weight = models.FloatField(max_length=100, null=True, blank=True)
    height = models.FloatField(max_length=100, null=True, blank=True)
    regno = models.CharField(max_length=50, null=True, blank=True)
    rchid = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.regno






