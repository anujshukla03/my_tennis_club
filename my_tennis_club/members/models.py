from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.contrib.auth.models import 


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20, unique=True)



class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    role = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

