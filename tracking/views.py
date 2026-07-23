from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import FoodMoodLogForm
from .insights import build_insight_page_context
from .models import InsightSummary


@login_required
def emotion_food(request):
    form = FoodMoodLogForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        log = form.save(commit=False)
        log.user = request.user
        log.save()
        messages.success(request, 'Your restorative entry has been logged.')
        return redirect('journal')

    insight = InsightSummary.objects.filter(user=request.user).first()
    context = {
        'form': form,
        'insight': insight,
        'weekly_consistency': insight.weekly_consistency_score if insight else 0,
        'total_logs': insight.total_logs_count if insight else 0,
    }
    return render(request, 'tracking/emotion_food_logger.html', context)


@login_required
def progress_insight(request):
    insight = InsightSummary.objects.filter(user=request.user).first()
    context = build_insight_page_context(insight)
    return render(request, 'tracking/progress_insight.html', context)
