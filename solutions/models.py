from django.db import models
from django.conf import settings

class Solution(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='independent_solutions')
    title = models.CharField(max_length=255)
    target_area = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='solutions_gallery/')
    technical_file = models.FileField(upload_to='solutions_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Səsvermə üçün sahələr
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='solution_votes', blank=True)

    def total_votes(self):
        return self.votes.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='comments')
    # Bura related_name əlavə etdik
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='solution_comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"{self.user.username} - {self.solution.title}"