from django.db import models
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError


class Circle(models.Model):
    name = models.CharField(max_length=100, default="My Circle")
    collective_name = models.CharField(max_length=100, help_text="e.g., 'Oak & Stone' collective")
    description = models.TextField(help_text="A private space for walking toward restoration...")
    created_at = models.DateTimeField(auto_now_add=True)

    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="circles", blank=True)

    def __str__(self):
        return f"{self.name} - {self.collective_name}"

    def clean(self):
        if self.pk:
            count = self.members.count()
            if count < 4 or count > 6:
                raise ValidationError(f"A Circle must have between 4 and 6 members. Current size: {count}")
            
    def add_member(self, user):
        if self.members.count() >= 6:
            raise ValidationError("This circle is already full (max 6 members).")
        self.members.add(user)

    def remove_member(self, user):
        if self.members.count() <= 4:
            replacement = (
                CircleWaitlist.objects
                .filter(circle=self)
                .exclude(user=user)
                .order_by('joined_at')
                .first()
            )
            if not replacement:
                raise ValidationError(
                    "Cannot remove member — circle would fall below the minimum of 4, "
                    "and there's no one on the waitlist to backfill."
                )
            with transaction.atomic():
                self.members.add(replacement.user)
                self.members.remove(user)
                replacement.delete()
        else:
            self.members.remove(user)

class Message(models.Model):
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="circle_chats/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"From {self.sender.email} in {self.circle.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class WeeklyPrompt(models.Model):
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name="prompts")
    question = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt for {self.circle.name}: {self.question[:30]}..."


class PromptAnswer(models.Model):
    prompt = models.ForeignKey(WeeklyPrompt, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="prompt_answers")
    answer_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('prompt', 'user')

    def __str__(self):
        return f"{self.user.email}'s response to prompt"


class CircleWaitlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='waitlist')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['joined_at']
        unique_together = ('user', 'circle')

    def __str__(self):
        return f"{self.user} waiting for {self.circle}"