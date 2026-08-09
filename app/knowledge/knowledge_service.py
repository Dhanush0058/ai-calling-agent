from typing import List

from app.knowledge.knowledge_retriever import KnowledgeRetriever
from app.integrations.llm_client import LLMClient


class KnowledgeService:

    def __init__(self):
        self.retriever = KnowledgeRetriever()
        self.llm = LLMClient()

    def answer(self, question: str, top_k: int = 5) -> dict:
        hits = self.retriever.retrieve(question, top_k)

        # Build a prompt containing the most relevant policy snippets
        prompt_sections: List[str] = ["You are an assistant that answers questions using company policy documents."]
        if hits:
            prompt_sections.append("Relevant Policy Snippets:")
            for h in hits:
                text = h.get("text") or ""
                prompt_sections.append(f"- {text}")

        prompt_sections.append(f"Question: {question}")
        prompt_sections.append("Answer succinctly and cite the relevant snippet indexes when possible.")

        prompt = "\n\n".join(prompt_sections)

        response = self.llm.chat(prompt)

        return {"response": response, "hits": hits}
