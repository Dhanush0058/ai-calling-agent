from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate
from app.schemas.customer import CustomerUpdate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException



class CustomerService:

    def __init__(self):
        self.repository = CustomerRepository()

    def create_customer(
    self,
    db: Session,
    customer: CustomerCreate,
    current_user: User,
):

        try:
            return self.repository.create(
                db,
                customer,
                current_user.id
            )

        except IntegrityError:
            raise HTTPException(
                status_code=409,
                detail="Phone or Email already exists"
            )

    def get_all_customers(
    self,
    db: Session,
    current_user: User,
    search: str | None,
    sort: str | None,
    skip: int,
    limit: int,
):
        return self.repository.get_all(
            db,
            current_user.id,
            search,
            sort,
            skip,
            limit,
        )

    def get_customer_by_id(
    self,
    db: Session,
    customer_id: int,
    current_user: User,

):
        return self.repository.get_by_id(
        db,
        customer_id,
        current_user.id,
        
    )
    def update_customer(
        self,
        db: Session,
        customer_id: int,
        customer_data: CustomerUpdate,
         current_user: User,
    ):
        customer = self.repository.get_by_id(
            db,
            customer_id,
            current_user.id,
        )

        if customer is None:
            return None

        return self.repository.update(
            db,
            customer,
            customer_data,
        )
    def delete_customer(
    self,
    db: Session,
    customer_id: int,
    current_user: User,
):
        
        customer = self.repository.get_by_id(
            db,
            customer_id,
            current_user.id,
        )

        if customer is None:
            return None

        self.repository.delete(db, customer)

        return customer

    