from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_page, name='login'),
    path('signup', signup_page, name='signup'),
    path('dashboard', dashboard, name='dashboard'),
    path('journal', emotion_food_logger, name='journal'),
    path('insights', progress_insight, name='insights'),
    path('circle', my_circle, name='circle'),
    path('profile', profile_settings, name='profile'),
]

