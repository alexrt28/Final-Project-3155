from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_item"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    review_id = Column(Integer, ForeignKey("review.id"))
    order_item_id = Column(Integer, ForeignKey("order_item.id"))
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"))
    
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String(100), nullable=False)
    calories = Column(Integer)

    review = relationship("Review", back_populates="menu_item")
    order_item = relationship("OrderItem", back_populates="menu_item")
    ingredient = relationship("Ingredient", back_populates="menu_item")