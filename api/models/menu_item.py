from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class MenuItem(Base):
    __tablename__ = "menu_item"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String(100), nullable=False)
    calories = Column(Integer)

    recipes = relationship("Recipe", back_populates="menu_item")
    reviews = relationship("Review", back_populates="menu_item")
    order_items = relationship("OrderItem", back_populates="menu_item")
