from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import SignUpForm, CustomAuthenticationForm


def signup_view(request):
    if request.user.is_authenticated:
        return render(request, 'registration/error.html', {'user': request.user})
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        return render(request, 'registration/error.html', {'user': request.user})

    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Успешный логаут!')
        return redirect('home')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
