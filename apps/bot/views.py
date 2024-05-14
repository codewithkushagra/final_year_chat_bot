import json
import requests

from loguru import logger

from django.views import View
from django.views import generic
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from config.settings.local import TELEGRAM_API_URL, URL
from .models import ConversationHistory, ConversationRole
from .utils.mapper import message_to_conversation_history_user, message_to_conversation_history_model
from .utils.gemini import GeminiLLM


@method_decorator(csrf_exempt, name="dispatch")
class TelegramBotView(View):
    def post(self, request, *args, **kwargs):
        message = json.loads(request.body.decode("utf-8"))
        data = message_to_conversation_history_user(message, ConversationRole.USER)
        ConversationHistory.objects.create(**data)
        try:
            gemini = GeminiLLM()
            response = gemini.generate_response(
                chat_id=data.get("chat_id"), user_text=data.get("message")
            )
            data = message_to_conversation_history_model(message, response, ConversationRole.MODEL)
            ConversationHistory.objects.create(**data)
            self.send_message(
                "sendMessage",
                {
                    "chat_id": data.get("chat_id"),
                    "text": response,
                },
            )
        except Exception as e:
            logger.info(e)
        return HttpResponse("ok")

    def send_message(self, method, data):
        return requests.post(TELEGRAM_API_URL + method, data)


class SetWebhookView(View):
    def get(self, request, *args, **kwargs):
        response = requests.post(f"{TELEGRAM_API_URL}setWebhook?url={URL}").json()
        return HttpResponse(f"{response}")



class TelegramBotIntegration(generic.TemplateView):
    template_name = "pages/integrations/telegram/telegram.html"
