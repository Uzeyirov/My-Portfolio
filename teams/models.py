from django.db import models
from django.conf import settings
from innovation.models import Idea # İdeyalara bağlamaq üçün
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=255, verbose_name="Komanda Adı")
    name = models.CharField(max_length=255)
    # Yeni sahə: Kimləri axtardığımızı bura yazacağıq
    looking_for = models.CharField(max_length=255, blank=True, null=True, help_text="Məs: Backend, Designer, Marketer")
    description = models.TextField(verbose_name="Məqsəd və Fəaliyyət")
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_teams')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams_joined', blank=True)
    idea = models.ForeignKey(Idea, on_delete=models.SET_NULL, null=True, blank=True, related_name='project_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    is_looking_for_members = models.BooleanField(default=True, verbose_name="Üzv axtarılır")

    def __str__(self):
        return self.name

class JoinRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='membership_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(verbose_name="Müraciət mesajı")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Gözləmədə'),
        ('accepted', 'Qəbul edildi'),
        ('rejected', 'Rədd edildi')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user') # Bir nəfər eyni komandaya təkrar müraciət edə bilməsin


# teams/models.py

class TeamMessage(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] # Mesajlar vaxt sırası ilə düzülsün

    
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_image(self):
        # Faylın şəkil olub-olmadığını yoxlamaq üçün kiçik köməkçi
        if self.file:
            return self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
        return False

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'