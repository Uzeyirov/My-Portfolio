from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Qeydiyyatdan keçən istifadəçini dərhal sistemə daxil edirik
            login(request, user) 
            # İndi isə onu Login səhifəsinə yox, Ana Səhifəyə (home) atırıq
            return redirect('home') 
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'users/profile.html')