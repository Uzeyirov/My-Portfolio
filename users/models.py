from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Əlavə sahələrimiz
    is_student = models.BooleanField(default=False)
    is_manufacturer = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)
    karma = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username