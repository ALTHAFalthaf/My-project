from django.db import models

#Create your models here.
class Usertable(models.Model):

    fname = models.CharField(max_length=15)
    lname = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    dob   = models.DateField(default='2000-01-01')
    role =  models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(blank=True,null=True)