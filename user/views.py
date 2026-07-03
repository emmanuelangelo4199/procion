from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, SignupForm
from .models import User


def login_page(request):
    if request.user.is_authenticated:
        return redirect('login')  
    
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('login') 
        messages.error(request, 'Invalid email or password.')

    context = {'form': form}
    return render(request, "user/login_page.html", context)

def signup_page(request):
    if request.user.is_authenticated:
        return redirect('login') 
     
    form = SignupForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            name=form.cleaned_data['name'],
        )
        login(request, user)
        return redirect('login') 

    context = {'form':form}
    return render(request, "user/signup_page.html", context)

def profile_settings(request):

    context = {}
    return render(request, "user/profile_settings.html", context)

def logout_view(request):
    logout(request)
    return redirect('login')