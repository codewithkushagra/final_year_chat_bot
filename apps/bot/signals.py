from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Bot, BotStatus


@receiver(pre_save, sender=Bot)
def update_bot_status(sender, instance, **kwargs):
    if not instance.pk:
        return
    old_instance = sender.objects.get(pk=instance.pk)
    if old_instance.bot_url != instance.bot_url:
        instance.status = BotStatus.INACTIVE
