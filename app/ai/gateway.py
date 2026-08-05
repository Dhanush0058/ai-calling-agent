from sqlalchemy.orm import Session

from app.ai.context_builder import ContextBuilder
from app.ai.prompt_builder import PromptBuilder
from app.ai.response_formatter import ResponseFormatter
from app.integrations.gemini_client import GeminiClient
from app.tools.tool_executor import ToolExecutor


class AIGateway:

    def __init__(self):
        self.llm = GeminiClient()

    def process(
        self,
        message: str,
        db: Session,
        customer_id: int | None = None,
    ):

        executor = ToolExecutor(db)

        tool_result = executor.execute(
            message,
            customer_id,
        )

        context = ContextBuilder(
            db=db,
            customer_id=customer_id,
        ).build()

        prompt = PromptBuilder.build(
            message=message,
            context=context,
            tool_result=tool_result,
        )

        response = self.llm.chat(prompt)

        return ResponseFormatter.format(response)

