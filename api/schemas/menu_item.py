from pydantic import BaseModel
from typing import Optional

class MenuItemBase(BaseModel):
    name: str
    price: float
    category: str
    calories: int

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(MenuItemBase):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None


class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True