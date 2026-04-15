from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    menu_item_id = Column(Integer, ForeignKey("menu_item.id"))

    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    # unit = Column(Integer) # not sure what unit is vs. quantity

    menu_item = relationship("MenuItem", back_populates="ingredient")