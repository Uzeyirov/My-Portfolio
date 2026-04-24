from django.contrib import admin
from .models import Challenge, Submission

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'status', 'deadline', 'is_approved')
    list_filter = ('status', 'is_approved', 'submission_type')
    search_fields = ('title', 'organizer__username')
    list_editable = ('status', 'is_approved') # Birbaşa siyahıdan təsdiqləmək üçün

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('solver', 'challenge', 'score', 'created_at')
    list_filter = ('challenge',)
    search_fields = ('solver__username', 'challenge__title')