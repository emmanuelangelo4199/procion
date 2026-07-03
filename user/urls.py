from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_page, name='login'),
    path('signup', signup_page, name='signup'),
    path('profile', profile_settings, name='profile'),
]

