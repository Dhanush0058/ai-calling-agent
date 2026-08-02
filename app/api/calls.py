from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.call import (
    CallCreate,
    CallEnd,
    CallResponse,
)

from app.services.call_service import CallService

router = APIRouter(
    prefix="/calls",
    tags=["Calls"],
)

service = CallService()


@router.post(
    "",
    response_model=CallResponse,
    status_code=201,
)
def start_call(
    call: CallCreate,
    db: Session = Depends(get_db),
):

    return service.start_call(
        db,
        call,
    )


@router.put(
    "/{call_id}",
    response_model=CallResponse,
)
def end_call(
    call_id: int,
    call: CallEnd,
    db: Session = Depends(get_db),
):

    result = service.end_call(
        db,
        call_id,
        call,
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Call not found",
        )

    return result


@router.get(
    "",
)
def get_all_calls(
    db: Session = Depends(get_db),
):

    return service.get_all_calls(
        db,
    )


@router.get(
    "/{call_id}",
    response_model=CallResponse,
)
def get_call(
    call_id: int,
    db: Session = Depends(get_db),
):

    result = service.get_call(
        db,
        call_id,
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Call not found",
        )

    return result


@router.delete(
    "/{call_id}",
)
def delete_call(
    call_id: int,
    db: Session = Depends(get_db),
):

    result = service.delete_call(
        db,
        call_id,
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Call not found",
        )

    return {
        "message": "Call deleted successfully"
    }