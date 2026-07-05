from django.contrib import admin
from .models import FoodMoodLog, InsightSummary


@admin.register(FoodMoodLog)
class FoodMoodLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'emotion', 'created_at')
    list_filter = ('emotion', 'created_at')
    search_fields = ('user__email', 'food_description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(InsightSummary)
class InsightSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'weekly_consistency_score', 'total_logs_count', 'last_computed')
    search_fields = ('user__email',)
    readonly_fields = ('last_computed',)
