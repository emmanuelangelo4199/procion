from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, SignupForm
from .models import User, UserProfile


def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid email or password.')

    context = {'form': form}
    return render(request, "user/login_page.html", context)


def signup_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
     
    form = SignupForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            name=form.cleaned_data['name'],
        )
        login(request, user)
        return redirect('onboarding')

    context = {'form': form}
    return render(request, "user/signup_page.html", context)



@login_required
def profile_settings(request):
    context = {}
    return render(request, "user/profile_settings.html", context)


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def onboarding_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            request.user.name = name
            request.user.save()

        dob_str = request.POST.get('date_of_birth', '').strip()
        if dob_str:
            try:
                profile.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        profile.bio = request.POST.get('bio', '').strip()

        weight_unit = request.POST.get('weight_unit', 'kg')
        cur_weight_raw = request.POST.get('current_weight', '').strip()
        goal_weight_raw = request.POST.get('goal_weight', '').strip()

        if cur_weight_raw:
            try:
                val = float(cur_weight_raw)
                profile.current_weight = round(val * 0.453592, 1) if weight_unit == 'lbs' else val
            except ValueError:
                pass

        if goal_weight_raw:
            try:
                val = float(goal_weight_raw)
                profile.goal_weight = round(val * 0.453592, 1) if weight_unit == 'lbs' else val
            except ValueError:
                pass

        height_unit = request.POST.get('height_unit', 'cm')
        if height_unit == 'cm':
            h_raw = request.POST.get('height_metric', '').strip()
            if h_raw:
                try:
                    profile.height = float(h_raw)
                except ValueError:
                    pass
        else:
            ft_raw = request.POST.get('height_ft', '').strip()
            in_raw = request.POST.get('height_in', '').strip()
            if ft_raw:
                try:
                    feet = float(ft_raw)
                    inches = float(in_raw) if in_raw else 0.0
                    profile.height = round(((feet * 12) + inches) * 2.54, 1)
                except ValueError:
                    pass

        activity_level = request.POST.get('activity_level', 'Sedentary')
        dietary_style = request.POST.get('dietary_style', 'Omnivore')
        triggers = request.POST.getlist('triggers')

        profile.preferences = {
            'activity_level': activity_level,
            'dietary_style': dietary_style,
            'triggers': triggers,
        }
        profile.save()

        messages.success(request, 'Welcome to Porcion! Your onboarding is complete.')
        return redirect('dashboard')

    context = {
        'profile': profile,
    }
    return render(request, "user/onboarding_view.html", context)


