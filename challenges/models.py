from django.db import models
from django.conf import settings  # Bura dəyişdi
from django.utils import timezone

class Challenge(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Aktiv (Həllər qəbul edilir)'),
        ('JUDGING', 'Qiymətləndirmə (Deadline bitib)'),
        ('FINISHED', 'Bitmiş (Qaliblər elan edilib)'),
    )

    SUBMISSION_TYPE_CHOICES = (
        ('FILE', 'Yalnız Fayl'),
        ('LINK', 'Yalnız Link (GitHub, Figma və s.)'),
        ('BOTH', 'Həm Fayl, Həm Link'),
    )

    # Bura dəyişdi: settings.AUTH_USER_MODEL
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_challenges')
    title = models.CharField(max_length=255, verbose_name="Yarışın Adı")
    description = models.TextField(verbose_name="Problemin Təsviri")
    reward = models.CharField(max_length=100, blank=True, null=True, verbose_name="Mükafat")
    
    deadline = models.DateTimeField(verbose_name="Son Tarix (Deadline)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    submission_type = models.CharField(max_length=10, choices=SUBMISSION_TYPE_CHOICES, default='BOTH')
    
    is_approved = models.BooleanField(default=False, verbose_name="Admin Təsdiqi")
    created_at = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False) # Görüntüdən silinmə üçün

    def __str__(self):
        return self.title

    @property
    def is_past_deadline(self):
        return timezone.now() > self.deadline

class Submission(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='submissions')
    
    # Bura dəyişdi: settings.AUTH_USER_MODEL
    solver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_submissions')
    
    file_submission = models.FileField(upload_to='submissions/files/', blank=True, null=True, verbose_name="Həll Faylı")
    link_submission = models.URLField(max_length=500, blank=True, null=True, verbose_name="Həll Linki")
    description = models.TextField(blank=True, verbose_name="Həll haqqında qısa izah")
    
    score = models.IntegerField(default=0, verbose_name="Münsif Xalı")
    feedback = models.TextField(blank=True, null=True, verbose_name="Münsif Rəyi")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.solver.username} - {self.challenge.title}"
    
    class Meta:
        ordering = ['-score', 'created_at']