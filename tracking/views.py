from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import FoodMoodLogForm
from .insights import build_insight_page_context
from .models import InsightSummary, JournalEntry, FoodMoodLog, Emotion
from django.core.paginator import Paginator
 

@login_required
def emotion_food(request):
    form = FoodMoodLogForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        log = form.save(commit=False)
        log.user = request.user
        log.save()
        messages.success(request, 'Your restorative entry has been logged.')
        return redirect('emotion')

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


@login_required
def journal_new(request):
    if request.method == 'POST':
        entry = JournalEntry.objects.create(
            user=request.user,
            title=request.POST.get('title', ''),
            emotion=request.POST.get('emotion', ''),
            gratitude=request.POST.get('gratitude', ''),
            reflection=request.POST.get('reflection', ''),
            healing_intention=request.POST.get('healing_intention', ''),
            photo=request.FILES.get('photo'),
        )
        return redirect('journal_detail', pk=entry.pk)

    return render(request, 'tracking/journal_entry.html', {
        'emotions': Emotion.choices,
    })


@login_required
def journal_history(request):
    entries = JournalEntry.objects.filter(user=request.user)
    paginator = Paginator(entries, 12)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'tracking/journal_history.html', {
        'entries': page,
    })


@login_required
def journal_detail(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    return render(request, 'tracking/journal_detail.html', {
        'entry': entry,
    })


@login_required
def journal_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('journal_history')
    return redirect('journal_detail', pk=pk)

