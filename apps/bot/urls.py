from django.urls import path

from .views import (
    TelegramBotView,
    SetWebhookView,
    TelegramBotIntegration,
    CreateTelegramBot,
)

app_name = "bot"

urlpatterns = [
    path("getchats/<int:id>/", TelegramBotView.as_view(), name="telegram-bot"),
    path("setwebhook/<int:id>/", SetWebhookView.as_view(), name="setwebhook"),
    path("telegram/", TelegramBotIntegration.as_view(), name="bot_list"),
    path("telegram/create/", CreateTelegramBot.as_view(), name="create_bot"),
]
