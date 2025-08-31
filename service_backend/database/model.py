from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from service_backend.database.db import Base
import uuid

class UserTwo(Base):
    __tablename__ = "user_two"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    lastname = Column(String(255))
    email = Column(String(255))
    age = Column(String(255))
    city = Column(String(255))