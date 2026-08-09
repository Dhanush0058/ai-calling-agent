import logging

import requests

from app.core.config import settings


logger = logging.getLogger(__name__)


class OpenRouterClient:

    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.url = settings.OPENROUTER_API_URL or "https://openrouter.ai/api/v1/chat/completions"
        self.model = settings.OPENROUTER_MODEL or "openai/gpt-oss-20b:free"
        self.reasoning_enabled = settings.OPENROUTER_REASONING

    def chat(self, prompt: str):
        if not self.api_key:
            return "(no-openrouter-key) stubbed response"

        logger.info(
            "Using OpenRouter model=%s url=%s reasoning=%s",
            self.model,
            self.url,
            self.reasoning_enabled,
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }

        if self.reasoning_enabled:
            payload["reasoning"] = {"enabled": True}

        response = requests.post(self.url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        logger.info("OpenRouter response status=%s", response.status_code)

        # OpenRouter chat completion responses use the OpenAI message format
        return data["choices"][0]["message"]["content"]
