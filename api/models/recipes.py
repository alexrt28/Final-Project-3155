from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    menu_item_id = Column(Integer, ForeignKey("menu_item.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"))

    amount = Column(Integer, index=True, nullable=False, server_default='0.0')

    menu_item = relationship("MenuItem", back_populates="recipes")
    ingredient = relationship("Ingredient", back_populates="recipes")