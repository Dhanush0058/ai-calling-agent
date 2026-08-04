from datetime import datetime

from sqlalchemy.orm import Session

from app.models.call import Call


class CallTools:

    @staticmethod
    def get_call_history(db: Session):
        return db.query(Call).order_by(Call.created_at.desc()).all()

    @staticmethod
    def get_last_call(db: Session):
        return (
            db.query(Call)
            .order_by(Call.created_at.desc())
            .first()
        )

    @staticmethod
    def get_call_summary(db: Session, call_id: int):
        call = db.query(Call).filter(Call.id == call_id).first()
        return call.summary if call else None

    @staticmethod
    def create_call(db: Session, customer_id: int):
        new_call = Call(
            customer_id=customer_id,
            created_at=datetime.utcnow(),
        )
        db.add(new_call)
        db.commit()
        db.refresh(new_call)
        return new_call

    @staticmethod
    def save_summary(
        db: Session,
        call_id: int,
        summary: str,
        sentiment: str | None = None,
        intent: str | None = None,
        transcript: str | None = None,
        embedding_id: str | None = None,
    ):
        call = db.query(Call).filter(Call.id == call_id).first()
        if call is None:
            return None

        call.summary = summary
        if sentiment is not None:
            call.sentiment = sentiment
        if intent is not None:
            call.intent = intent
        if transcript is not None:
            call.transcript = transcript
        if embedding_id is not None:
            call.embedding_id = embedding_id

        db.commit()
        db.refresh(call)
        return call
