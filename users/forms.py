from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bütün xanalara Bootstrap klası əlavə edirik
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['is_student', 'is_manufacturer']:
                field.widget.attrs['class'] = 'form-check-input' # Checkbox-lar üçün

    class Meta:
        model = User
        fields = ('username', 'email', 'is_student', 'is_manufacturer')