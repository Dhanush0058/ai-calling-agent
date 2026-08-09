try:
    from google import genai
except Exception:  # pragma: no cover - optional dependency in constrained envs
    genai = None

from app.core.config import settings


class GeminiClient:

    def __init__(self):

        # Defensive: don't construct the real client in environments without an API key
        # Tests and CI can run without a GEMINI_API_KEY set.
        if not settings.GEMINI_API_KEY or genai is None:
            self.client = None
            return

        try:
            self.client = genai.Client(
                api_key=settings.GEMINI_API_KEY,
            )
        except Exception:
            self.client = None

    def chat(
        self,
        prompt: str,
    ):

        if self.client is None:
            # Return a benign stub response when no API key is configured or the SDK is unavailable.
            return "(gemini unavailable) stubbed response"

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text
        except Exception:
            return "(gemini unavailable) stubbed response"