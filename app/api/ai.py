from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.ai.gateway import AIGateway

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

gateway = AIGateway()


@router.post("/chat")
def chat(
    message: str,
    db: Session = Depends(get_db),
):

    # TODO: replace with authenticated user id when auth is available
    response = gateway.process(
        message=message,
        db=db,
        customer_id=None,
    )

    return response