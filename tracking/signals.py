from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .insights import recompute_insight_summary
from .models import FoodMoodLog


@receiver(post_save, sender=FoodMoodLog)
def refresh_insights_on_log_save(sender, instance, **kwargs):
    recompute_insight_summary(instance.user)


@receiver(post_delete, sender=FoodMoodLog)
def refresh_insights_on_log_delete(sender, instance, **kwargs):
    recompute_insight_summary(instance.user)
