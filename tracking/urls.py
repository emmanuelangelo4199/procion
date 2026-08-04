from django.urls import path
from .views import emotion_food, progress_insight, journal_history, journal_new, journal_detail, journal_delete

urlpatterns = [
    path('emotion_logger', emotion_food, name='emotion'),
    path('insights', progress_insight, name='insights'),
    path('journal', journal_history, name='journal_history'),
    path('journal/new/', journal_new, name='journal_new'),
    path('journal/<int:pk>/', journal_detail, name='journal_detail'),
    path('journal/<int:pk>/delete/', journal_delete, name='journal_delete'),
]
 