from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    # Occupation sahəsini formda göstərmək üçün əlavə edirik
    occupation = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Nə işlə məşğulsunuz? (məs: Tələbə, Mühəndis)'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # BURANI DƏYİŞDİR: Köhnə is_student və is_manufacturer-i sil, occupation-ı əlavə et
        fields = ('username', 'email', 'occupation') 

    # Əgər əlavə stillər vermək istəyirsənsə __init__ metodunu saxlaya bilərsən
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})