from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerTools:

    @staticmethod
    def get_customer_by_name(
        db: Session,
        name: str,
    ):
        return (
            db.query(Customer)
            .filter(Customer.name.ilike(f"%{name}%"))
            .first()
        )

    @staticmethod
    def get_all_customers(
        db: Session,
    ):
        return db.query(Customer).all()

    @staticmethod
    def customer_count(db: Session):
        return db.query(Customer).count()