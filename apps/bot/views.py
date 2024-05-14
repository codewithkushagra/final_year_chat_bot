import json
import requests

from loguru import logger

from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from config.settings.local import TELEGRAM_API_URL, URL
from .models import ConversationHistory, ConversationRole
from .utils.mapper import message_to_conversation_history


@method_decorator(csrf_exempt, name="dispatch")
class TelegramBotView(View):
    def post(self, request, *args, **kwargs):
        message = json.loads(request.body.decode("utf-8"))
        data = message_to_conversation_history(message, ConversationRole.USER)
        ConversationHistory.objects.create(**data)
        try:
            self.send_message(
                "sendMessage", {"chat_id": data.get("chat_id"), "text": f"Your message: {data.get('message')}"}
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
