from django.shortcuts import render



def landing_page(request):

    context = {}

    return render(request, "app/landing_page.html", context)

def dashboard(request):

    context = {}
    return render(request, "app/dashboard.html", context)