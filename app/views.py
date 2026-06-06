from django.shortcuts import render, redirect



def landing_page(request):

    context = {}

    return render(request, "app/landing_page.html", context)

def login_page(request):

    context = {}
    return render(request, "app/login_page.html", context)

def signup_page(request):

    context = {}
    return render(request, "app/signup_page.html", context)

def dashboard(request):

    context = {}
    return render(request, "app/dashboard.html", context)

def emotion_food_logger(request):

    context = {}
    return render(request, "app/emotion_food_logger.html", context)

def progress_insight(request):

    context = {}
    return render(request, "app/progress_insight.html", context)

def my_circle(request):

    context = {}
    return render(request, "app/my_circle.html", context)

def profile_settings(request):

    context = {}
    return render(request, "app/profile_settings.html", context)