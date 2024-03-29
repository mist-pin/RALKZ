from django.db import models
from django.contrib.auth.models import AbstractUser

class RalkzUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, primary_key=True)
    phone = models.CharField(max_length=10)
    address = models.TextField(max_length=200)
    email = models.EmailField(max_length=30, unique=True, null=True)
    full_name = models.CharField(max_length=30, default="NULL")
    accept_privacy_policy = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_aspirant = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    pass_hist = models.TextField(max_length=10000) #password history

    REQUIRED_FIELDS = ['phone',  'full_name', 'email']
    USERNAME_FIELD = "username"