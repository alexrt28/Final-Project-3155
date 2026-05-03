from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PromoCodeBase(BaseModel):
    code: str = Field(alias='promo_code')
    discount: float
    discount_type: str
    expiry: datetime

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

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