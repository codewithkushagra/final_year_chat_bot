from datetime import date, timedelta

from django import forms
from django.core.exceptions import ValidationError

from .models import Bot


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ["bot_token", "bot_username", "bot_name", "bot_url"]
        widgets = {
            "bot_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Bot Name"}
            ),
            "bot_username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Username Name"}
            ),
            "bot_url": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Bot URL"}
            ),
            "bot_token": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Token"}
            ),
        }

    def save(self, commit=True, *args, **kwargs):
        bot = super().save(commit=False)
        print("jjjjkakskjnska", kwargs.get("user", None))
        bot.user = kwargs.get("user", None)
        print(bot.user)
        if commit:
            bot.save()
        return bot
