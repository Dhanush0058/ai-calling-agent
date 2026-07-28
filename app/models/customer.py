from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100))

    phone: Mapped[str] = mapped_column(String(15), unique=True)

    email: Mapped[str] = mapped_column(String(100), unique=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )