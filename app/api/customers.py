from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import status
from app.core.dependencies import get_current_user
from app.models.user import User
from typing import Literal

from app.database.dependencies import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)
from app.services.customer_service import CustomerService

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

service = CustomerService()


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=201,
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_customer(db, customer,current_user)

@router.get(
    "",
    response_model=list[CustomerResponse],
)
def get_customers(
    search: str | None = None,
    sort: Literal[
    "name",
    "-name",
    "email",
    "-email"
    ] | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
        return service.get_all_customers(
            db,
            current_user,
            search,
            sort,
            skip,
            limit,
        )

@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = service.get_customer_by_id(
        db,
        customer_id,
        current_user,
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer

@router.put(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = service.update_customer(
        db,
        customer_id,
        customer_data,
        current_user,
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    return customer

@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = service.delete_customer(
        db,
        customer_id,
        current_user,
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )