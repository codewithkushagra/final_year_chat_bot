from django.db import models


class ConversationRole(models.TextChoices):
    USER = ("usr", "user")
    MODEL = ("mod", "model")


class ConversationHistory(models.Model):
    chat_id = models.CharField(max_length=1024, null=True, blank=True)
    message_id = models.CharField(max_length=1024, null=True, blank=True)
    username = models.CharField(max_length=1024, null=True, blank=True)
    role = models.CharField(
        max_length=64, choices=ConversationRole.choices, default=ConversationRole.MODEL
    )
    message = models.CharField(max_length=4096)
    timestamp = models.DateTimeField(auto_now=True)
    metadata = models.JSONField(default=None, null=True, blank=True)
