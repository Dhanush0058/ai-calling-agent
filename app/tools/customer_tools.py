from sqlalchemy.orm import Session
from app.models.customer import Customer


class CustomerTools:

    @staticmethod
    def customer_count(db: Session) -> int:
        return db.query(Customer).count()

    @staticmethod
    def get_customer_by_name(db: Session, name: str):

        customer = (
            db.query(Customer)
            .filter(Customer.name.ilike(f"%{name}%"))
            .first()
        )

        if customer is None:
            return None

        return {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
        }