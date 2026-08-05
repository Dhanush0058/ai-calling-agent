from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.call import Call


class ProfileService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def get_profile(
        self,
        customer_id: int,
    ):

        customer = (
            self.db.query(Customer)
            .filter(
                Customer.id == customer_id
            )
            .first()
        )

        if customer is None:
            return {}

        call_count = (
            self.db.query(Call)
            .filter(
                Call.customer_id == customer_id
            )
            .count()
        )

        return {
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "call_count": call_count,
        }

