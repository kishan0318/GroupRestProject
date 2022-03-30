from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser,AbstractUser

# Create your models here.

class Student(models.Model):
    pass

TITLE_CHOICES = [
    ('1', 'Superuser_user'),
    ('2', 'teacher'),
    ('3','Student')
]

class User(AbstractUser):
    
    user_type=models.CharField(max_length=20,choices=TITLE_CHOICES)
    mobile=models.CharField(max_length=11)
    gender=models.CharField(max_length=5,choices=(('1','Male'),('2', 'Female')))
    image=models.ImageField(upload_to='profile_image')
    branch=models.CharField(max_length=20,choices=(('1','Machenical'),('2', 'IT'),('3', 'Automobile'),('4', 'Others')),default='4')
    
    def __str__(self):
        return self.username
