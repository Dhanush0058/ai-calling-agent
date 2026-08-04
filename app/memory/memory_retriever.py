from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.call import Call


class MemoryRetriever:

    def __init__(self, window_days: int = 30, max_calls: int = 5):
        self.window_days = window_days
        self.max_calls = max_calls

    def fetch_recent_calls(self, db: Session, customer_id: int):
        cutoff = datetime.utcnow() - timedelta(days=self.window_days)
        return (
            db.query(Call)
            .filter(Call.customer_id == customer_id)
            .filter(Call.created_at >= cutoff)
            .order_by(Call.created_at.desc())
            .limit(self.max_calls)
            .all()
        )
