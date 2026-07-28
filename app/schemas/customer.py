from pydantic import BaseModel, ConfigDict, EmailStr,Field, field_validator


class CustomerCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
        description="Customer name"
    )

    phone: str = Field(
        min_length=10,
        max_length=10,
        description="10 digit phone number"
    )

    email: EmailStr
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        return value
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str):

        if not value.isdigit():
            raise ValueError("Phone must contain only digits")

        if len(value) != 10:
            raise ValueError("Phone must be exactly 10 digits")

        return value

class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        value = value.strip()
    
        if not value:
            raise ValueError("Name cannot be empty")
    
        return value
    
    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is None:
            return value

        if not value.isdigit():
            raise ValueError("Phone must contain only digits")

        if len(value) != 10:
            raise ValueError("Phone must be exactly 10 digits")

        return value

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class CustomerListResponse(BaseModel):
    items: list[CustomerResponse]
    total: int
    skip: int
    limit: int
