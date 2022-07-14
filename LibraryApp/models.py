from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Register(AbstractUser):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
    USER = (('Student','Student'),('Librarian','Librarian'))
    usertype = models.CharField(max_length=255,choices=USER)
    name = models.CharField(max_length=255)
    dob = models.DateField()
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    degree = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Books(models.Model):
    title = models.CharField(max_length=255)
    auther = models.CharField(max_length=255)



