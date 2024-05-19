from django.contrib import admin

from .models import ConversationHistory, Message, Bot

admin.site.register(ConversationHistory)
admin.site.register(Message)
admin.site.register(Bot)
