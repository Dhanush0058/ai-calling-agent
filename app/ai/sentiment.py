from app.integrations.llm_client import LLMClient


class Sentiment:

    LABELS = [
        "POSITIVE",
        "NEGATIVE",
        "NEUTRAL",
        "ANGRY",
        "CONFUSED",
    ]

    def __init__(self):
        self.llm = LLMClient()

    def analyze(self, summary: str) -> str:
        prompt = f"""
You are an AI sentiment analyzer for customer support summaries.

Summary:
{summary}

Return exactly one sentiment label from the following list:
{', '.join(self.LABELS)}
"""
        response = self.llm.chat(prompt).strip().upper()
        for label in self.LABELS:
            if label in response:
                return label
        return "NEUTRAL"
