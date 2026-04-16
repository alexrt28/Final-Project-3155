from typing import Optional
from pydantic import BaseModel


class RecipeBase(BaseModel):
    quantity: float
    unit: str


class RecipeCreate(RecipeBase):
    menu_item_id: int
    ingredient_id: int

class RecipeUpdate(BaseModel):
    quantity: Optional[float] = None
    unit: Optional[str] = None

class Recipe(RecipeBase):
    id: int
    menu_item_id: int
    ingredient_id: int

    class ConfigDict:
        from_attributes = True