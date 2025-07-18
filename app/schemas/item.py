# Defines the SQLAlchemy model for the database schema.

from sqlalchemy import Column, Integer, String, Float, Boolean
from app.core.database import Base

class ItemDB(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    print = Column(Float)
    is_available = Column(Boolean, default=True)