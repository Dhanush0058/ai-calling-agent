import uuid

from app.embedding.embedding_service import EmbeddingService
from app.ai.sentiment import Sentiment
from app.ai.summarizer import Summarizer
from app.integrations.llm_client import LLMClient
from app.tools.call_tools import CallTools


class CallProcessor:

    INTENT_LABELS = [
        "Complaint",
        "Refund",
        "Technical Support",
        "Billing",
        "Delivery",
        "General Inquiry",
    ]

    def __init__(self):
        self.summarizer = Summarizer()
        self.sentiment = Sentiment()
        self.embeddings = EmbeddingService()
        self.llm = LLMClient()

    def extract_intent(self, summary: str) -> str:
        prompt = f"""
You are an AI intent classifier for customer support summaries.

Summary:
{summary}

Choose exactly one label from the following list:
{', '.join(self.INTENT_LABELS)}
"""
        response = self.llm.chat(prompt).strip()
        normalized = response.upper()
        for label in self.INTENT_LABELS:
            if label.upper() in normalized:
                return label
        return "General Inquiry"

    def process_call(self, db, call_id: int, transcript: str):
        summary = self.summarizer.summarize(transcript)
        sentiment_label = self.sentiment.analyze(summary)
        intent_label = self.extract_intent(summary)

        embedding_result = self.embeddings.embed([summary])[0]
        embedding_id = self.embeddings.store(
            summary=summary,
            embedding=embedding_result,
            metadata={"call_id": str(call_id)},
        )

        call = CallTools.save_summary(
            db=db,
            call_id=call_id,
            summary=summary,
            sentiment=sentiment_label,
            intent=intent_label,
            transcript=transcript,
            embedding_id=embedding_id,
        )

        return {
            "call": call,
            "summary": summary,
            "sentiment": sentiment_label,
            "intent": intent_label,
            "embedding_id": embedding_id,
            "embedding": embedding_result.vector,
            "embedding_metadata": {
                "model": embedding_result.model,
                "provider": embedding_result.provider,
                "dimensions": embedding_result.dimensions,
            },
        }
