from sqlalchemy.orm import Session

from app.integrations.gemini_client import GeminiClient
from app.memory.memory_service import MemoryService
from app.tools.tool_executor import ToolExecutor


class AIAgent:

    def __init__(self):
        self.llm = GeminiClient()
        self.memory_service = MemoryService()

    def ask(
        self,
        message: str,
        db: Session,
        customer_id: int | None = None,
    ):
        executor = ToolExecutor(db)
        tool_result = executor.execute(message, customer_id=customer_id)

        memory_context = None
        if customer_id is not None:
            memory_context = self.memory_service.get_customer_memory(db, customer_id)

        if tool_result:
            prompt = f"""
You are an AI customer support assistant.

Customer Memory:
{memory_context or 'No recent calls found.'}

Database Result:
{tool_result}

Current Question:
{message}
"""
            return self.llm.chat(prompt)

        if memory_context:
            prompt = f"""
{memory_context}

Current Question:
{message}
"""
            return self.llm.chat(prompt)

        return self.llm.chat(message)
