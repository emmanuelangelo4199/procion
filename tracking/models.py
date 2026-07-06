from django.db import models
from django.conf import settings


class Emotion(models.TextChoices):
    STRESSED = 'STRESSED', 'Stressed'
    BORED = 'BORED', 'Bored'
    CALM = 'CALM', 'Calm'
    HAPPY = 'HAPPY', 'Happy'
    SAD = 'SAD', 'Sad'
    TIRED = 'TIRED', 'Tired'


class FoodMoodLog(models.Model):
    """Captures data from the 'Restorative Entry' form."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='food_mood_logs'
    )
    emotion = models.CharField(
        max_length=20,
        choices=Emotion.choices,
        help_text="The primary mood selected by the user."
    )
    food_description = models.TextField(
        help_text="Sensory description of flavors, textures, or warmth."
    )
    food_image = models.ImageField(
        upload_to='mindful_meals/%Y/%m/%d',  # fixed: removed stray "-"
        null=True,
        blank=True,
        help_text="Optional captured picture of the meal snapshot."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Food & Mood Log"
        verbose_name_plural = "Food & Mood Logs"

    def __str__(self):
        return f"{self.user.email} - {self.emotion} ({self.created_at.strftime('%Y-%m-%d')})"


class InsightSummary(models.Model):
    """Feeds aggregated trends to the 'Pattern Deep-Dive' analytics dashboard."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='insight_summary'
    )
    weekly_consistency_score = models.IntegerField(
        default=0,
        help_text="Percentage score (e.g. 85 = 85% consistency this week)."
    )
    total_logs_count = models.PositiveIntegerField(
        default=0,
        help_text="Total logs submitted over time."
    )
    mood_correlation_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Maps moods to sensory word frequencies."
    )
    last_computed = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Insight Summary"
        verbose_name_plural = "Insight Summaries"

    def __str__(self):
        return f"Analytics Summary for {self.user.email}"
