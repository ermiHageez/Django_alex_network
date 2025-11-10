# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_startup = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
