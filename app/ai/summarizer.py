from app.integrations.llm_client import LLMClient


class Summarizer:

    def __init__(self):
        self.llm = LLMClient()

    def summarize(self, transcript: str) -> str:
        prompt = f"""
You are an AI assistant that extracts a concise customer-support summary from a spoken call transcript.

Transcript:
{transcript}

Summary:
"""
        return self.llm.chat(prompt).strip()
