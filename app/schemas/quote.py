from pydantic import BaseModel
from typing import List

class QuoteItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total: float

class QuoteResponse(BaseModel):
    tender_id: int
    tender_title: str
    items: List[QuoteItem]
    total_price: float
