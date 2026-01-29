from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Integer, Text
from app.db.base import Base

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    # preferences can be a JSON string or plain text
    preferences = Column(Text, nullable=True) 
