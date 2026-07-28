from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr

class CustomerUpdate(BaseModel):
    name: str
    phone: str
    email: EmailStr

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

