from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import LoginForm

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home_page')
            else:
                return render(request, 'auth/login.html',
                              {"error": "Login yoki parol noto'g'ri!"})
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

@login_required(login_url='login_page')
def logout_page(request):
    logout(request)
    return redirect('login_page')
