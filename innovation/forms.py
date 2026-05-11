from django import forms
from .models import Idea

# forms.py faylında
class IdeaForm(forms.ModelForm):
    # Kateqoriyanı seçim yox, mətn sahəsi kimi təyin edirik
    category = forms.CharField(
        max_length=100, 
        required=False, # Məcburi olmasın istəyirsənsə False et
        label="Kateqoriya"
    )

    class Meta:
        model = Idea
        fields = ['title', 'category', 'description', 'image', 'is_official_product']

    def save(self, commit=True):
        instance = super().save(commit=False)
        category_name = self.cleaned_data.get('category')
        
        if category_name:
            # Əgər bu adda kateqoriya varsa onu götürür, yoxdursa yenisini yaradır
            from .models import Category # Model adını özünə görə dəqiqləşdir
            cat_obj, created = Category.objects.get_or_create(name=category_name)
            instance.category = cat_obj
        else:
            instance.category = None # Məcburi deyilsə boş qala bilər
            
        if commit:
            instance.save()
        return instance
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