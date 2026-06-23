from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Circle
from django.db.models.signals import pre_delete
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import CircleWaitlist

@receiver(m2m_changed, sender=Circle.members.through)
def enforce_circle_size_limits(sender, instance, action, pk_set, **kwargs):
    """Hard guard: enforce the 4-6 member range, even via shell/admin."""
    if action == "pre_add":
        potential_count = instance.members.count() + len(pk_set)
        if potential_count > 6:
            raise ValueError(
                f"Cannot add members. Circle limit is 6 (attempted: {potential_count})."
            )
    elif action == "pre_remove":
        potential_count = instance.members.count() - len(pk_set)
        if potential_count < 4:
            raise ValueError(
                f"Cannot remove members. Circle minimum is 4 (attempted: {potential_count})."
            )


User = get_user_model()

@receiver(pre_delete, sender=User)
def backfill_circle_on_user_delete(sender, instance, **kwargs):
    user = instance

    for circle in user.circles.all():
        remaining_count = circle.members.count() - 1  # this user hasn't been removed yet
        if remaining_count < 4:
            replacement = CircleWaitlist.objects.filter(circle=circle).exclude(user=user).order_by('joined_at').first()
            if replacement:
                with transaction.atomic():
                    circle.members.add(replacement.user)
                    replacement.delete()