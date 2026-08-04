from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.agents.ai_agent import AIAgent

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

agent = AIAgent()


@router.post("/chat")
def chat(
    message: str,
    db: Session = Depends(get_db),
):

    response = agent.ask(
        message,
        db,
    )

    return {
        "response": response,
    }