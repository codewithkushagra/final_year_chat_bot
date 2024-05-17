from django.contrib import admin

from .models import ConversationHistory, Message

admin.site.register(ConversationHistory)
admin.site.register(Message)
