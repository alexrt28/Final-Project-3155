from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    quantity = Column(Integer, index=True, nullable=False)
    subtotal = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_item")
    menu_item = relationship("MenuItem", back_populates="order_item")

