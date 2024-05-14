import google.generativeai as genai


class GeminiConfig:
    def __init__(
        self, temperature=1, top_p=0.95, top_k=0, max_output_tokens=4096
    ) -> None:
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.max_output_tokens = max_output_tokens

    def get_configs(self):
        return vars(self)


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


class GeminiLLM:
    def __init__(self, model_name="gemini-1.5-pro-latest") -> None:
        self.model_name = model_name
        self.model_configs = GeminiConfig().get_configs()
        self.model_safety_setting = GeminiSafetySettings().get_safety_settings()

    def model_init(self):
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.model_configs,
            safety_settings=self.model_safety_setting,
        )
