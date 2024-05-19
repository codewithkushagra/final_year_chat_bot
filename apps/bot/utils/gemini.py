from loguru import logger
import google.generativeai as genai
from qdrant_client import QdrantClient

from config.settings.local import GEMINI_API_KEY, EMBEDDING_MODEL
from apps.bot.models import Message, ConversationRole

QDRANTDB_HOST = "localhost"
QDRANTDB_PORT = 6333


class GeminiConfig:
    RETRIEVAL_QUERY = "retrieval_query"
    RETRIEVAL_DOCUMENT = "retrieval_document"
    SEMANTIC_SIMILARITY = "semantic_similarity"
    CLASSIFICATION = "classification"
    CLUSTERING = "clustering"

    def __init__(
        self, temperature=1, top_p=0.95, top_k=0, max_output_tokens=4096
    ) -> None:
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.max_output_tokens = max_output_tokens

    def get_configs(self):
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "max_output_tokens": self.max_output_tokens,
        }


class GeminiSafetySettings:
    def __init__(self, safety_settings=None) -> None:
        self._initial_value = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ]
        self.safety_settings = (
            safety_settings if safety_settings else self._initial_value
        )

    def add_setting(self, category, threshold):
        self.safety_settings.append(
            {
                "category": category,
                "threshold": threshold,
            }
        )

    def remove__setting_by_category(self, category):
        index_to_remove = next(
            (
                index
                for index, item in enumerate(self.safety_settings)
                if item["category"] == category
            ),
            None,
        )
        if index_to_remove is not None:
            del self.safety_settings[index_to_remove]
            print(f"Removed: {category}")
        else:
            print(f"No category found with the name: {category}")

    def get_safety_settings(self):
        return self.safety_settings


class GeminiSystemInstructions:
    def __init__(self, system_instruction=[]) -> None:
        self.system_instruction = self.get_instruction_set()

    def get_instruction_set(self):
        return [
            "You are a customer support agent for company ZOMATO",
            "You have to answer customer querry based on ZOMATO company data and related products",
            "For generic questions unrelated to ZOMATO company don't answer",
            "Give response in less than 40 words",
        ]


class GeminiLLM:
    DEFAULT_MESSAGE = (
        "Sorry, I was unable to understand your text, please explain in detail."
    )

    def __init__(self, model_name="gemini-1.5-pro-latest") -> None:
        genai.configure(api_key=GEMINI_API_KEY)
        self.model_name = model_name
        self.model_configs = GeminiConfig().get_configs()
        self.model_safety_setting = GeminiSafetySettings().get_safety_settings()
        self.system_instruction = GeminiSystemInstructions().get_instruction_set()
        self.model_init()

    def model_init(self):
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.model_configs,
            safety_settings=self.model_safety_setting,
            system_instruction=self.system_instruction,
        )

    def get_conversation_history(self, chat_id, user_text):
        logger.info(chat_id)
        history = (
            Message.objects.filter(conversation_history__chat_id=chat_id)
            .values("message", "role")
            .order_by("-timestamp")[:10]
        )
        client = QdrantClient(host=QDRANTDB_HOST, port=QDRANTDB_PORT)
        embedding = GeminiLLM.generate_embeddings(text=user_text)
        search_result = client.search(
            collection_name="zomato_vector", query_vector=embedding, limit=2
        )
        results = [
            {"parts": result.payload.get("data"), "role": "model"}
            for result in search_result
        ]
        history = [
            {
                "parts": [item.get("message")],
                "role": ConversationRole(item.get("role")).label,
            }
            for item in reversed(history)
        ]
        history = results + history
        logger.info(history)
        return history

    def generate_response(self, chat_id, user_text):
        conversation = self.model.start_chat(
            history=self.get_conversation_history(chat_id=chat_id, user_text=user_text)
        )
        try:
            result = conversation.send_message(user_text)
            return result._result.candidates[0].content.parts[0].text
        except Exception as e:
            logger.info(e)
            return self.DEFAULT_MESSAGE

    @staticmethod
    def generate_embeddings(text=None, task_type=GeminiConfig.SEMANTIC_SIMILARITY):
        genai.configure(api_key=GEMINI_API_KEY)
        try:
            if text:
                return genai.embed_content(
                    model=EMBEDDING_MODEL,
                    content=text,
                    task_type=task_type,
                )["embedding"]
            logger.info("Empty string passed for generating embedding")
            return []
        except Exception as e:
            logger.info(f"Error: {e}")
            return []
