from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TenderBase(BaseModel):
    zakupki_id: str = Field(..., description="Unique Tender Number (№ закупки)")
    title: str = Field(..., description="Title or description of the tender")
    max_price: Optional[str] = Field(None, description="Initial maximum contract price")
    publish_date: Optional[str] = Field(None, description="Date of publication")
    customer_name: Optional[str] = Field(None, description="Organization/Customer name")
    link: str = Field(..., description="Full URL to the tender page")

class TenderCreate(TenderBase):
    pass

class TenderInDB(TenderBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ScrapedTenderList(BaseModel):
    tenders: List[TenderCreate]
