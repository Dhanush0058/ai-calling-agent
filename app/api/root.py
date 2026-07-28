from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "AI Calling Agent API is running!"
    }
