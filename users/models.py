from django.contrib.auth.models import AbstractUser

from django.db import models

class User(AbstractUser):
    # Köhnə Boolean sahələri əvəzinə sərbəst yazı sahəsi
    occupation = models.CharField(max_length=100, blank=True, null=True, verbose_name="Vəzifə/Tələbə")
    bio = models.TextField(max_length=500, blank=True)
    karma = models.IntegerField(default=0)
    
    # Əgər profil şəkli birbaşa User-dədirsə (AbstractUser istifadə etdiyin üçün):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username