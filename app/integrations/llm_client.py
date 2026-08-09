from app.core.config import settings
from app.integrations.openrouter_client import OpenRouterClient
from app.integrations.gemini_client import GeminiClient


class LLMClient:

    def __init__(self):
        if settings.OPENROUTER_API_KEY:
            self.client = OpenRouterClient()
        else:
            self.client = GeminiClient()

    def chat(self, prompt: str):
        return self.client.chat(prompt)
