from __future__ import absolute_import, unicode_literals

import logging
import requests
from celery import shared_task

from .models import (
    ConversationProcessing,
    ConversationRole,
    ConversationHistory,
    ConversationProcessingStatus,
    Message,
)
from .utils.mapper import (
    message_to_conversation_history,
    tele_user_message_to_message_model,
    tele_model_message_to_message_model,
)
from config.settings.local import TELEGRAM_API_URL
from .utils.gemini import GeminiLLM


logger = logging.getLogger(__name__)


def send_generated_reply(method, data):
    logger.info(f"sending message: {data}" )
    return requests.post(TELEGRAM_API_URL + method, data)


@shared_task()
def generate_and_send_response(process_id):
    process = ConversationProcessing.objects.get(id=process_id)
    message = process.message_data
    data = message_to_conversation_history(message)

    conversation_history, _ = ConversationHistory.objects.get_or_create(**data)
    model_message_data = tele_user_message_to_message_model(
        message, conversation_history, ConversationRole.USER
    )
    Message.objects.create(**model_message_data)
    try:
        gemini = GeminiLLM()
        response = gemini.generate_response(
            chat_id=conversation_history.chat_id,
            user_text=model_message_data.get("message"),
        )
        model_message_data = tele_model_message_to_message_model(
            message, conversation_history, response, ConversationRole.MODEL
        )
        Message.objects.create(**model_message_data)
        send_generated_reply(
            "sendMessage",
            {
                "chat_id": conversation_history.chat_id,
                "text": response,
            },
        )
        process.processing_status = ConversationProcessingStatus.COMPLETED
        process.save()
        logger.info("Success")
    except Exception as e:
        logger.info(f"Error: {e}")
        process.processing_status = ConversationProcessingStatus.FAILED
