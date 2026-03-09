from django import forms
from .models import Idea

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        # Müəllif (author) və səs (votes) avtomatik olacaq, ona görə onları bura yazmırıq
        fields = ['title', 'category', 'description', 'image', 'is_official_product']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'İdeyanızı ətraflı izah edin...'}),
        }

from .models import Idea, Comment # Comment-i bura əlavə et

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control border-0 bg-light',
                'placeholder': 'Fikrinizi bölüşün və ya sual verin...',
                'rows': '3',
                'style': 'border-radius: 15px; resize: none;'
            }),
        }

from django import forms
from django.contrib.auth.models import User  # Bu vacibdir!
from .models import Idea, Comment, Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User  # Burada dırnaq işarəsi OLMAMALIDIR
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-pill'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control rounded-pill'}),
            'bio': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control rounded-pill'}),
        }