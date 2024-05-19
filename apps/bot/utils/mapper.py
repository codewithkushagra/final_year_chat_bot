def message_to_conversation_history(message, bot_id):
    mapped_data = {
        "chat_id": message["message"]["chat"]["id"],
        "bot_id": bot_id,
        "username": message["message"]["from"]["username"]
    }
    return mapped_data


def tele_user_message_to_message_model(message, conversation_history, role):
    mapped_data = {
        "conversation_history_id": conversation_history.id,
        "message_id": message["message"]["message_id"],
        "username": message["message"]["from"]["username"],
        "role": role,
        "message": message["message"]["text"],
        "metadata": message,
    }
    return mapped_data


def tele_model_message_to_message_model(message, conversation_history, response, role):
    mapped_data = {
        "conversation_history_id": conversation_history.id,
        "username": "bot",
        "role": role,
        "message": response,
    }
    return mapped_data
