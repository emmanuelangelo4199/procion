from django.urls import path
from .views import login_page, signup_page, profile_settings, onboarding_view

urlpatterns = [
    path('login', login_page, name='login'),
    path('signup', signup_page, name='signup'),
    path('profile', profile_settings, name='profile'),
    path('onboarding', onboarding_view, name='onboarding'),
]

