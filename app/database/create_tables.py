from app.database.base import Base
from app.database.database import engine

from app.models.customer import Customer
from app.models.user import User

print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")