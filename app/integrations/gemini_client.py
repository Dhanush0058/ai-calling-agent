from google import genai

from app.core.config import settings


class GeminiClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

    def chat(
        self,
        prompt: str,
    ):

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text