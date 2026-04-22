from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PromoCodeBase(BaseModel):
    code: str
    discount: float
    discount_type: str
    expiry: datetime

class PromoCodeCreate(PromoCodeBase):
    pass

class PromoCodeUpdate(BaseModel):
    code: Optional[str] = None
    discount: Optional[float] = None
    expiry: Optional[datetime] = None

class PromoCode(PromoCodeBase):
    id: int

    class ConfigDict:
        from_attributes = True