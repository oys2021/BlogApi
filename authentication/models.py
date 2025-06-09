from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    ROLE_CHOICES = [
        ('User', 'User'),
        ('Admin', 'Admin'),
    ]

    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='User')
    full_name= models.CharField(max_length=50)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    # is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

