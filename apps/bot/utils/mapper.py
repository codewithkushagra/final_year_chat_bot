def message_to_conversation_history(message, role):
    mapped_data = {
        "chat_id": message["message"]["chat"]["id"],
        "message_id": message["message"]["message_id"],
        "username": message["message"]["from"]["username"],
        "role": role,
        "message": message["message"]["text"],
        "metadata": message,
    }
    return mapped_data
