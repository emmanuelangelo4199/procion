from django.shortcuts import render


def my_circle(request):

    context = {}
    return render(request, "circle/my_circle.html", context)