import json
import requests

from loguru import logger

from django.views import View
from django.views import generic
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.utils.utils import CSRFExemptMixin, SideBarSelectedMixin
from config.settings.local import TELEGRAM_API_URL, URL
from apps.bot.models import ConversationProcessing, Bot, BotStatus
from apps.bot.forms import BotForm
from apps.bot.tasks import generate_and_send_response


class TelegramBotView(CSRFExemptMixin, View):
    def post(self, request, *args, **kwargs):
        bot_id = kwargs.get("id")
        message = json.loads(request.body.decode("utf-8"))
        print(message)
        process = ConversationProcessing.objects.create(message_data=message)
        generate_and_send_response.delay(process.id, bot_id)
        return HttpResponse("ok")


class SetWebhookView(View):
    def get(self, request, *args, **kwargs):
        bot_id = kwargs.get("id")
        try:
            bot = Bot.objects.get(id=bot_id)
        except Bot.DoesNotExist:
            return JsonResponse({"error": "Bot not found"}, status=404)
        try:
            response = requests.post(
                f"{TELEGRAM_API_URL}{bot.bot_token}/setWebhook?url={bot.bot_url}/bot/getchats/{bot.id}/"
            ).json()
        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
        print(response)
        if response.get("ok"):
            bot.status = BotStatus.ACTIVE
            bot.save()
            return JsonResponse(
                {"message": "Webhook set successfully", "details": response}, status=200
            )
        else:
            return JsonResponse(
                {"error": "Failed to set webhook", "details": response}, status=500
            )


class TelegramBotIntegration(
    LoginRequiredMixin, SideBarSelectedMixin, generic.ListView
):
    template_name = "pages/integrations/telegram/telegram.html"
    model = Bot
    context_object_name = "bot_list"
    success_url = "bot:bot_list"
    parent = "bot"
    segment = "bot_list"
    paginate_by = 6


class CreateTelegramBot(LoginRequiredMixin, SideBarSelectedMixin, generic.FormView):
    template_name = "pages/integrations/telegram/create_bot.html"
    form_class = BotForm
    parent = "bot"
    segment = "bot_list"
    success_url = reverse_lazy("bot:bot_list")

    def get_context_data(self, **kwargs):
        context = super(CreateTelegramBot, self).get_context_data(**kwargs)
        context["parent"] = self.parent
        context["segment"] = self.segment
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            bot = form.save(user=request.user)
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
