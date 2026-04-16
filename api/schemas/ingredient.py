from typing import Optional
from pydantic import BaseModel


class IngredientBase(BaseModel):
    name: str
    quantity: int
    unit: int

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(IngredientBase):
    name: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[int] = None

class Ingredient(IngredientBase):
    id: int

    class ConfigDict:
        from_attributes = True

