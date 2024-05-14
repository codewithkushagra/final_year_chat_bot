from django.urls import path

from .views import TelegramBotView, SetWebhookView


urlpatterns = [
    path('getchats/', TelegramBotView.as_view(), name='telegram-bot'),
    path('setwebhook/', SetWebhookView.as_view(), name='setwebhook'),
]
