from google import genai

from app.core.config import settings


class GeminiClient:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

    def chat(
        self,
        messages: list[dict],
    ) -> str:

        prompt = ""

        for message in messages:
            prompt += f"{message['role']}: {message['content']}\n"

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text