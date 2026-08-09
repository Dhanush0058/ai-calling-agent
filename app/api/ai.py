from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.ai.gateway import AIGateway

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

@router.post("/chat")
def chat(
    message: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    gateway = AIGateway()

    response = gateway.process(
        message=message,
        db=db,
        user_id=current_user.id,
    )

    return response