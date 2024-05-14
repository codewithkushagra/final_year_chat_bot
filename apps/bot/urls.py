from django.urls import path

from .views import TelegramBotView, SetWebhookView, TelegramBotIntegration


app_name = 'bot'

urlpatterns = [
    path('getchats/', TelegramBotView.as_view(), name='telegram-bot'),
    path('setwebhook/', SetWebhookView.as_view(), name='setwebhook'),
    path('telegram/', TelegramBotIntegration.as_view(), name='telegram_integration')
]
