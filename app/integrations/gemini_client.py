from google import genai

from app.core.config import settings


class GeminiClient:

    def __init__(self):

        # Defensive: don't construct the real client in environments without an API key
        # Tests and CI can run without a GEMINI_API_KEY set.
        if not settings.GEMINI_API_KEY:
            self.client = None
            return

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

    def chat(
        self,
        prompt: str,
    ):

        if self.client is None:
            # Return a benign stub response when no API key is configured.
            return "(no-gemini-key) stubbed response"

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text