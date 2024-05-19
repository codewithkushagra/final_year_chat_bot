from django.db import models

from apps.user.models import User


class BotPlatform(models.TextChoices):
    TELEGRAM = ("TELE", "Telegram")


class BotStatus(models.TextChoices):
    INACTIVE = ("inactive", "In Active")
    ACTIVE = ("active", "Active")
    FAILED = ("failed", "Failed")


class Bot(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    bot_token = models.CharField(max_length=4096)
    bot_type = models.CharField(
        max_length=8, choices=BotPlatform.choices, default=BotPlatform.TELEGRAM
    )
    bot_username = models.CharField(
        max_length=1024, default=None, null=True, blank=True
    )
    bot_name = models.CharField(max_length=4096, default=None, null=True, blank=True)
    bot_url = models.CharField(max_length=4096, default=None, null=True, blank=True)
    status = models.CharField(
        max_length=8, choices=BotStatus.choices, default=BotStatus.INACTIVE
    )
    created_at = models.DateTimeField(auto_now=True)


class ConversationRole(models.TextChoices):
    USER = ("usr", "user")
    MODEL = ("mod", "model")


class ConversationHistory(models.Model):
    chat_id = models.CharField(max_length=1024, null=True, blank=True)
    username = models.CharField(max_length=1024, null=True, blank=True)
    bot = models.ForeignKey(
        Bot, on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    timestamp = models.DateTimeField(auto_now=True)


class Message(models.Model):
    conversation_history = models.ForeignKey(
        ConversationHistory, null=True, blank=True, on_delete=models.CASCADE
    )
    message_id = models.CharField(max_length=1024, null=True, blank=True)
    username = models.CharField(max_length=1024, null=True, blank=True)
    role = models.CharField(
        max_length=64, choices=ConversationRole.choices, default=ConversationRole.MODEL
    )
    message = models.CharField(max_length=4096)
    timestamp = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=None, null=True, blank=True)


class ConversationProcessingStatus(models.TextChoices):
    PENDING = ("pend", "pending")
    COMPLETED = ("comp", "completed")
    FAILED = ("fail", "failed")


class ConversationProcessing(models.Model):
    message_data = models.JSONField(default=None, null=True, blank=True)
    processing_status = models.CharField(
        max_length=8,
        choices=ConversationProcessingStatus.choices,
        default=ConversationProcessingStatus.PENDING,
    )
    conversation_history = models.ForeignKey(
        ConversationHistory,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
