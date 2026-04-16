from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    rating: int
    comment: str

class ReviewCreate(ReviewBase):
    customer_id: int
    menu_item_id: int

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

class Review(ReviewBase):
    id: int
    customer_id: int
    menu_item_id: int

    class ConfigDict:
        from_attributes = True