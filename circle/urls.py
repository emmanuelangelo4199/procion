from django.urls import path
from .views import my_circle, leave_circle

urlpatterns = [
     path('', my_circle, name='circle'),
     path('leave', leave_circle, name='leave_circle'),
]