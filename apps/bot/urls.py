from django.urls import path

from .views import TelegramBotView, SetWebhookView, TelegramBotIntegration, ManageTelegramBot, IngestData

app_name = 'bot'

urlpatterns = [
    path('getchats/', TelegramBotView.as_view(), name='telegram-bot'),
    path('setwebhook/', SetWebhookView.as_view(), name='setwebhook'),
    path('telegram/', TelegramBotIntegration.as_view(), name='telegram_integration'),
    path('telegram/manage/', ManageTelegramBot.as_view(), name='manage_bot'),
    path('data_ingestion/', IngestData.as_view(), name='ingest_data')
]
