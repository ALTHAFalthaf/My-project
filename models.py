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
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CHILD, 'Child'),
        (DOCTOR, 'Doctor'),
        
    ]


    GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female')
    )

    # Fields for custom user roles
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=CHILD)  # Default role for regular users
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)
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







class VaccinationSchedule(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine_name = models.CharField(max_length=100)
    dose_number = models.IntegerField()
    given_date = models.DateField()
    next_due_date = models.DateField()

    def __str__(self):
        return f"{self.user.first_name}'s {self.vaccine_name} - Dose {self.dose_number}"










class Record(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Add other fields as needed...

 

class RecordView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

TIME = (
    ('B', 'Birth'),
    ('6w', '6 weeks (Infants)'),
    ('10w', '10 weeks (Infants)'),
    ('14w', '14 weeks (Infants)'),
    ('6m', '6 moonths (Infants)'),
    ('9m', '9 months (Infants)'),
    ('12m', '12-24 months (Infants)'),
    ('15m', '15-18 months (Infants)'),
    ('24m', '24 months (Infants)'),
    ('L', 'Less than 13 years '),
)


class Timing(models.Model):
    title = models.CharField(max_length=200)
    age = models.CharField(max_length=30)
    schedule_done = models.ForeignKey('Schedule', related_name='schedules_done', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return

class Immunogen(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    definition = models.CharField(max_length=100, blank=True, null=True)
    disease_handled = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.definition

    def __unicode__(self):
        return 
    # Your existing Immunogen model...

class Vaccine(models.Model):
    timing = models.CharField(max_length=20, choices=TIME)
    imu_id = models.ForeignKey('Immunogen', related_name='imus', on_delete=models.CASCADE)
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.imu_id.definition

    def get_absolute_url(self):
        return reverse('detail-vaccine', kwargs={'pk': self.pk})

    @property
    def usage(self):
        return self.schedule_set.count()

class Schedule(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    record = models.ForeignKey(Record, related_name='schedules', on_delete=models.CASCADE)
    date_immunized = models.DateTimeField(default=timezone.now)
    vaccine_type = models.ForeignKey(Vaccine, related_name='vaccines', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    exp_date = models.DateTimeField(blank=True, null=True)
    

    def __str__(self):
        return self.vaccine_type.imu_id.name

    def get_update_url(self):
        return reverse('schedule-update', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('schedule-detail', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('schedule-delete', kwargs={'pk': self.pk})