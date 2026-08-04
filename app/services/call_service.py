from datetime import datetime

from sqlalchemy.orm import Session

from app.ai.call_processor import CallProcessor
from app.models.call import Call
from app.schemas.call import CallCreate, CallEnd


class CallService:

    def start_call(
        self,
        db: Session,
        call: CallCreate,
    ):

        new_call = Call(
            customer_id=call.customer_id,
            created_at=datetime.utcnow(),
        )

        db.add(new_call)
        db.commit()
        db.refresh(new_call)

        return new_call

    def end_call(
        self,
        db: Session,
        call_id: int,
        call_data: CallEnd,
    ):

        call = db.query(Call).filter(
            Call.id == call_id
        ).first()

        if call is None:
            return None

        processor = CallProcessor()
        processor.process_call(
            db=db,
            call_id=call_id,
            transcript=call_data.transcript,
        )

        call.status = "completed"
        call.ended_at = datetime.utcnow()

        db.commit()
        db.refresh(call)

        return call

    def get_call(
        self,
        db: Session,
        call_id: int,
    ):

        return db.query(Call).filter(
            Call.id == call_id
        ).first()

    def get_all_calls(
        self,
        db: Session,
    ):

        return db.query(Call).all()

    def delete_call(
        self,
        db: Session,
        call_id: int,
    ):

        call = db.query(Call).filter(
            Call.id == call_id
        ).first()

        if call is None:
            return None

        db.delete(call)
        db.commit()

        return True