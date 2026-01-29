from sqlalchemy import Column, String, Integer, DateTime, Text, BigInteger
from sqlalchemy.sql import func
from app.db.base import Base

class Tender(Base):
    __tablename__ = "tenders"

    id = Column(Integer, primary_key=True, index=True)
    zakupki_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(Text, nullable=False)
    max_price = Column(Text, nullable=True) # Text to handle currency symbols/formats initially
    publish_date = Column(Text, nullable=True)
    customer_name = Column(Text, nullable=True)
    link = Column(Text, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
