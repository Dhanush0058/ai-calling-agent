from sqlalchemy.orm import Session

from app.rag.rag_service import RAGService
from app.tools.tool_executor import ToolExecutor


class AIGateway:

    def __init__(self):
        pass

    def process(
        self,
        message: str,
        db: Session,
        user_id: int | None = None,
        customer_id: int | None = None,
    ):

        executor = ToolExecutor(db)

        tool_result = executor.execute(
            message,
            user_id=user_id,
            customer_id=customer_id,
        )

        rag_service = RAGService(db=db, customer_id=customer_id)
        return rag_service.process(
            question=message,
            tool_result=tool_result,
        )

