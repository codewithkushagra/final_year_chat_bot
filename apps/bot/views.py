import json
import requests

from loguru import logger

from django.views import View
from django.views import generic
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from config.settings.local import TELEGRAM_API_URL, URL
from .models import ConversationProcessing
from apps.bot.tasks import generate_and_send_response


@method_decorator(csrf_exempt, name="dispatch")
class TelegramBotView(View):
    def post(self, request, *args, **kwargs):
        message = json.loads(request.body.decode("utf-8"))
        process = ConversationProcessing.objects.create(message_data=message)
        generate_and_send_response.delay(process.id)
        return HttpResponse("ok")


class SetWebhookView(View):
    def get(self, request, *args, **kwargs):
        response = requests.post(f"{TELEGRAM_API_URL}setWebhook?url={URL}").json()
        return HttpResponse(f"{response}")


class TelegramBotIntegration(generic.TemplateView):
    template_name = "pages/integrations/telegram/telegram.html"

class ManageTelegramBot(generic.TemplateView):
    template_name = "pages/integrations/telegram/create_bot.html"

class IngestData(generic.TemplateView):
    template_name = "pages/integrations/data_ingestion/data_ingestion.html"
