from typing import List

from sqlalchemy.orm import Session

from app.ai.context_builder import ContextBuilder
from app.ai.prompt_builder import PromptBuilder
from app.ai.response_formatter import ResponseFormatter
from app.integrations.llm_client import LLMClient
from app.rag.retriever import Retriever
from app.rag.reranker import Reranker
from app.models.call import Call


class RAGService:

    def __init__(self, db: Session, customer_id: int | None = None):
        self.db = db
        self.customer_id = customer_id
        self.retriever = Retriever(self.db)
        self.reranker = Reranker()
        self.llm = LLMClient()

    def process(self, question: str, tool_result: str):
        calls = self.retriever.retrieve(question)
        calls = self.reranker.rerank(calls, question)

        relevant_context = self._build_call_context(calls)
        context = ContextBuilder(
            db=self.db,
            customer_id=self.customer_id,
        ).build(relevant_calls=relevant_context)

        prompt = PromptBuilder.build(
            message=question,
            context=context,
            tool_result=tool_result,
        )

        response = self.llm.chat(prompt)
        return ResponseFormatter.format(response)

    def _build_call_context(self, calls: List[Call]) -> str:
        if not calls:
            return "No relevant calls found."

        sections = []
        for call in calls:
            sections.append(
                f"Call ID: {call.id}\nSummary: {call.summary or 'N/A'}\nIntent: {call.intent or 'N/A'}\nSentiment: {call.sentiment or 'N/A'}\nTranscript: {call.transcript or 'N/A'}"
            )
        return "\n---\n".join(sections)
