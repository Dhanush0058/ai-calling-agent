from fastapi import APIRouter

from app.agents.ai_agent import AIAgent

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

agent = AIAgent()


@router.post("/chat")
def chat(
    message: str,
):

    response = agent.ask(message)

    return {
        "response": response,
    }