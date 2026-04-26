from typing import Optional
from pydantic import BaseModel


class OrderItemBase(BaseModel):
    quantity: int
    subtotal: float = 0


class OrderItemCreate(OrderItemBase):
    order_id: int
    menu_item_id: int


class OrderItemUpdate(BaseModel):
    quantity: Optional[int] = None
    menu_item_id: Optional[int] = None


class OrderItem(OrderItemBase):
    id: int
    order_id: int
    menu_item_id: int

    class ConfigDict:
        from_attributes = True
