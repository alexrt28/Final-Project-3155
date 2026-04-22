from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel




class OrderBase(BaseModel):
    order_date: datetime
    order_type: str
    tracking_number: str
    status: str
    total_price: float

class OrderCreate(OrderBase):
    customer_id: int


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    customer_id: int

    class ConfigDict:
        from_attributes = True
