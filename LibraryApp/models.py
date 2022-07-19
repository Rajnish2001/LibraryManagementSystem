from re import L
from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from django.contrib.auth.hashers import make_password,is_password_usable,check_password
from datetime import datetime,timedelta


# Create your models here.
class Register(AbstractUser):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
    name = models.CharField(max_length=255,null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES,null=True)
    degree = models.CharField(max_length=255,null=True)
    email = models.EmailField(max_length=255, unique=True,null=True)
    password = models.CharField(max_length=255,null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        self.name

class Books(models.Model):
    title = models.CharField(max_length=255,null=True,unique=True)
    auther = models.CharField(max_length=255,null=True)
    price = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.title



class Student(models.Model):
    GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))
    name = models.CharField(max_length=255,null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES,null=True)
    degree = models.CharField(max_length=255,null=True)
    email = models.EmailField(max_length=255, unique=True,null=True)
    password = models.CharField(max_length=255,null=True)
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Student, self).save(*args, **kwargs)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)
    
    # def __str__(self):
    #     return self.name


# def expiry():
#     return datetime.today() + timedelta(days=14)
class Book_issues(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='student_name')
    books = models.ForeignKey(Books,on_delete=models.CASCADE,related_name='books')
    librarian = models.ForeignKey(Register,on_delete=models.CASCADE,related_name='librarian')
    date = models.DateField(auto_now_add=True)
    # expiry = models.DateTimeField(default=expiry)

    # def __str__(self):
    #     self.books.title

