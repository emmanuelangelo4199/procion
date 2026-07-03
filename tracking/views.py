from django.shortcuts import render

def emotion_food(request):
    context = {}
    return render(request, 'tracking/emotion_food_logger.html', context)

def progress_insight(request):
    context = {}
    return render(request, 'tracking/progress_insight.html', context)