from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate
from app.schemas.customer import CustomerUpdate
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, asc, desc
from fastapi import HTTPException, status


class CustomerRepository:
 #Creating tables
    def create(
    self,
    db: Session,
    customer: CustomerCreate,
    user_id: int,
):

        db_customer = Customer(
        name=customer.name,
        phone=customer.phone,
        email=customer.email,
        user_id=user_id,
    )

        db.add(db_customer)

        try:
            db.commit()
            db.refresh(db_customer)
            return db_customer

        except IntegrityError:
            db.rollback()
            raise

#Getting all the values
    def get_all(
    self,
    db: Session,
    user_id: int,
    search: str | None,
    email: str | None,
    phone: str | None,
    sort: str | None,
    skip: int,
    limit: int,
):
        
        query = (
            db.query(Customer)
            .filter(Customer.user_id == user_id)
        )


        # Search
        if search:
            query = query.filter(
                or_(
                    Customer.name.ilike(f"%{search}%"),
                    Customer.email.ilike(f"%{search}%"),
                )
            )
        if email:
            query = query.filter(
                Customer.email.ilike(f"%{email}%")
            )
        if phone:
            query = query.filter(
                Customer.phone.ilike(f"%{phone}%")
            )
        # Sorting
        sort_fields = {
        "name": Customer.name,
        "email": Customer.email,
        }

        if sort:
            descending = sort.startswith("-")
            field = sort.lstrip("-")

            if field not in sort_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid sort field '{sort}'. Allowed values: {', '.join(sort_fields.keys())}, -name, -email"
                )

            column = sort_fields[field]

            query = query.order_by(
                desc(column) if descending else asc(column)
            )
        total = query.count()

        customers = (
                query
                .offset(skip)
                .limit(limit)
                .all()
            )

        return {
            "items": customers,
            "total": total,
            "skip": skip,
            "limit": limit,
        }

#Getting by ID 
    def get_by_id(
    self,
    db: Session,
    customer_id: int,
    user_id: int,
):
        return (
            db.query(Customer)
            .filter(
                Customer.id == customer_id,
                Customer.user_id == user_id,
            )
            .first()
        )

#Updating the table values
    def update(
    self,
    db: Session,
    customer: Customer,
    customer_data: CustomerUpdate,
):
        
        customer.name = customer_data.name
        customer.phone = customer_data.phone
        customer.email = customer_data.email

        db.commit()
        db.refresh(customer)

        return customer

#Deleting from DataBases
    def delete(
        self,
        db: Session,
        customer: Customer,
    ):
        db.delete(customer)

        db.commit()
    