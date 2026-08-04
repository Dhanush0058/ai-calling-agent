from typing import List

from app.models.call import Call


class MemoryManager:

    @staticmethod
    def format_call_memory(call: Call) -> dict:
        return {
            "summary": call.summary,
            "sentiment": call.sentiment,
            "intent": call.intent,
            "date": call.created_at.isoformat() if call.created_at else None,
        }

    @staticmethod
    def build_memory_context(calls: List[Call]) -> str:
        if not calls:
            return "Customer Memory:\nNo recent calls found.\n"

        sections = ["Customer Memory:"]
        for index, call in enumerate(calls, start=1):
            sections.append(f"Call {index}")
            sections.append("Summary:")
            sections.append(call.summary or "No summary available.")
            sections.append("Sentiment:")
            sections.append(call.sentiment or "UNKNOWN")
            sections.append("Intent:")
            sections.append(call.intent or "UNKNOWN")
            sections.append(f"Date:\n{call.created_at.isoformat() if call.created_at else 'UNKNOWN'}")
            sections.append("-----------------")

        return "\n".join(sections)
