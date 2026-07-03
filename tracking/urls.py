from django.urls import path
from .views import emotion_food, progress_insight

urlpatterns = [
    path('journal', emotion_food, name='journal'),
    path('insights', progress_insight, name='insights'),
]
