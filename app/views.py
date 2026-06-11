from django.shortcuts import render, redirect


def landing_page(request):

    context = {}

    return render(request, "app/landing_page.html", context)