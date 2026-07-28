from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.schemas.user import (
    UserCreate,
    UserLogin,
    Token,
)

class AuthService:

    def __init__(self):
        self.repository = UserRepository()

    def register(
        self,
        db: Session,
        user_data: UserCreate,
    ):
        existing_user = self.repository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered",
            )

        user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hash_password(
                user_data.password
            ),
        )

        return self.repository.create(
            db,
            user,
        )
    
    def login(
    self,
    db: Session,
    user_data: UserLogin,
):
        
        user = self.repository.get_by_email(
        db,
        user_data.email,
    )
        

        if not user or not verify_password(
            user_data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            {
                "sub": user.email,
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )

    
        