from django.contrib import admin
from .models import Circle, Message, WeeklyPrompt, PromptAnswer, CircleWaitlist

admin.site.register(Circle)
admin.site.register(Message)
admin.site.register(WeeklyPrompt)
admin.site.register(PromptAnswer)
admin.site.register(CircleWaitlist)
