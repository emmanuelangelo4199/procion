from django.shortcuts import render


def login_page(request):

    context = {}
    return render(request, "user/login_page.html", context)

def signup_page(request):

    context = {}
    return render(request, "user/signup_page.html", context)

def dashboard(request):

    context = {}
    return render(request, "user/dashboard.html", context)

def emotion_food_logger(request):

    context = {}
    return render(request, "user/emotion_food_logger.html", context)

def progress_insight(request):

    context = {}
    return render(request, "user/progress_insight.html", context)

def my_circle(request):

    context = {}
    return render(request, "user/my_circle.html", context)

def profile_settings(request):

    context = {}
    return render(request, "user/profile_settings.html", context)