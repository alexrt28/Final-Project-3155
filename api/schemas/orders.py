from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class OrderLineItemCreate(BaseModel):
    menu_item_id: int
    quantity: int


class OrderBase(BaseModel):
    order_type: str
    promo_code_id: Optional[int] = None
    status: Optional[str] = None
    delivery_address: Optional[str] = None


class OrderCreate(OrderBase):
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    is_guest: bool = False
    items: List[OrderLineItemCreate]


class OrderUpdate(BaseModel):
    order_type: Optional[str] = None
    status: Optional[str] = None
    promo_code_id: Optional[int] = None
    delivery_address: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_number: str
    total_price: float
    customer_id: int

    class ConfigDict:
        from_attributes = True
