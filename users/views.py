from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # form.save() avtomatik olaraq username, email və occupation-ı bazaya yazacaq
            form.save() 
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hesab yaradıldı: {username}! İndi daxil ola bilərsiniz.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')