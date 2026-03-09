from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kateqoriya Adı")
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Kateqoriyalar"

class Idea(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ideas')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='ideas', blank=True)
    title = models.CharField(max_length=255, verbose_name="İdeya Başlığı")
    description = models.TextField(verbose_name="Ətraflı İzah")
    
    # İstehsalçı və ya fərdi fərqi
    is_official_product = models.BooleanField(default=False, verbose_name="Rəsmi Məhsuldur?")
    image = models.ImageField(upload_to='ideas/%Y/%m/%d/', blank=True, null=True, verbose_name="Şəkil/Render")
    
    # Səsvermə (Qarşılıqlı əlaqə)
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='idea_votes', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_votes(self):
        return self.votes.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='idea_comments'
    )
    content = models.TextField(verbose_name="Rəyiniz")
    # Cavab yazmaq üçün yeni sahə:
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # Müzakirə ardıcıllığı üçün köhnədən yeniyə

    def __str__(self):
        return f"{self.author.username} - {self.content[:20]}"
    
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Haqqında")
    location = models.CharField(max_length=100, blank=True, verbose_name="Məkan")
    # Gələcəkdə bura avatar = models.ImageField(...) əlavə edə bilərik
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True, null=True)


    def __str__(self):
        return f"{self.user.username} profili"

# İstifadəçi qeydiyyatdan keçən kimi avtomatik Profil yaradan funksiyalar (Signals)
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




class Solution(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='solutions')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='idea_solutions'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='solutions_images/', null=True, blank=True)
    file = models.FileField(upload_to='solutions_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author.username}"