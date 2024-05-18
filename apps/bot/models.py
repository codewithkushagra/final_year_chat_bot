from django.db import models


class ConversationRole(models.TextChoices):
    USER = ("usr", "user")
    MODEL = ("mod", "model")


class ConversationHistory(models.Model):
    chat_id = models.CharField(max_length=1024, null=True, blank=True)
    username = models.CharField(max_length=1024, null=True, blank=True)
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


class BotPlatform(models.TextChoices):
    TELEGRAM = ("TELE", "Telegram")


class Bot(models.Model):
    bot_token = models.CharField(max_length=4096)
    bot_type = models.CharField()
