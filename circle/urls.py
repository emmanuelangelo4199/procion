from django.urls import path
from .views import *

urlpatterns = [
     path('circle', my_circle, name='circle'),
]
