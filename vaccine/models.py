from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib import admin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, role=None,dob=None,**extra_fields):
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

        return self.create_user(email, password, role=role, dob=dob, **extra_fields)

class CustomUser(AbstractUser):
    ADMIN = 'Admin'
    CHILD = 'Child'
    DOCTOR = 'Doctor'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CHILD, 'Child'),
        (DOCTOR, 'Doctor'),
    ]

    # Fields for custom user roles
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=CHILD)  # Default role for regular users
    forget_password_token = models.UUIDField(null=True, blank=True) #forgetpass
    email = models.EmailField(unique=True)
    objects = CustomUserManager()
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=150)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    # Define boolean fields for specific roles
    is_child = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)

    def __str__(self):
        return self.email