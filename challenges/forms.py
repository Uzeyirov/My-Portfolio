from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file_submission', 'link_submission', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Həlliniz haqqında qısa qeydlər...',
                'rows': 4
            }),
            'link_submission': forms.URLInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'GitHub və ya Figma linki'
            }),
            'file_submission': forms.FileInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary'
            }),
        }



from .models import Challenge # Submission-dan əlavə bunu da import et

class ChallengeCreateForm(forms.ModelForm):
    class Meta:
        model = Challenge
        # Admin təsdiqi və statusu istifadəçidən gizlədirik
        fields = ['title', 'description', 'reward', 'deadline', 'submission_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Yarışın başlığı'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Problemi ətraflı izah edin...'}),
            'reward': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'placeholder': 'Məs: 100 AZN və ya Sertifikat'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control bg-dark text-white border-secondary', 'type': 'datetime-local'}),
            'submission_type': forms.Select(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
        }


class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['score', 'feedback'] # 'feedback' sahəsini modelə əlavə etməlisən
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control bg-dark text-white', 'min': '0', 'max': '100'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control bg-dark text-white', 'rows': 2}),
        }