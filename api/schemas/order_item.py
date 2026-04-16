from typing import Optional
from pydantic import BaseModel



class OrderItemBase(BaseModel):
    quantity: int
    subtotal: float


class OrderItemCreate(OrderItemBase):
    order_id: int
    menu_item_id: int

class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    subtotal: Optional[float] = None

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    menu_item_id: int

    class ConfigDict:
        from_attributes = True