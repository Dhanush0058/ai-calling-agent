from sqlalchemy.orm import Session
from app.models.customer import Customer


class CustomerTools:

    @staticmethod
    def customer_count(db: Session, user_id: int | None = None) -> int:
        query = db.query(Customer)
        if user_id is not None:
            query = query.filter(Customer.user_id == user_id)
        return query.count()

    @staticmethod
    def get_all_customers(db: Session, user_id: int | None = None):
        query = db.query(Customer)
        if user_id is not None:
            query = query.filter(Customer.user_id == user_id)

        customers = query.all()
        return [
            {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
            }
            for customer in customers
        ]

    @staticmethod
    def get_customer_by_name(db: Session, name: str, user_id: int | None = None):

        query = db.query(Customer).filter(Customer.name.ilike(f"%{name}%"))
        if user_id is not None:
            query = query.filter(Customer.user_id == user_id)

        customer = query.first()

        if customer is None:
            return None

        return {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
        }