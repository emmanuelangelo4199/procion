from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import Circle


@login_required 
def my_circle(request): 
    circle = request.user.circles.prefetch_related('members__profile').first()
    recent_messages = []
    if circle:
        recent_messages = circle.messages.select_related('sender').order_by('-created_at')[:50]
        recent_messages = reversed(recent_messages)

    context = {
        'circle': circle,
        'recent_messages': recent_messages
        }
    return render(request, "circle/my_circle.html", context)

@login_required
def leave_circle(request):
    circle = request.user.circles.first()
    if circle is None:
        messages.error(request, "You're not currently in a circle.")
        return redirect('circle')

    if request.method == "POST":
        try:
            circle.remove_member(request.user)
            messages.success(request, "You've left the circle.")
        except ValidationError as e:
            messages.error(request, " ".join(e.messages))
    return redirect('circle')