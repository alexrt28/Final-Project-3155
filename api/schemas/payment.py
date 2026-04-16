from typing import Optional
from pydantic import BaseModel


class PaymentBase(BaseModel):
    payment_type: str
    card_info: str
    status: str

class PaymentCreate(PaymentBase):
    order_id: int

class PaymentUpdate(BaseModel):
    payment_type: Optional[str] = None
    card_info: Optional[str] = None
    status: Optional[str] = None

class Payment(PaymentBase):
    id: int
    order_id: int

    class ConfigDict:
        from_attributes = True