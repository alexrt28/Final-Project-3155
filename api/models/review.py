from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_item.id"))
    customer_id = Column(Integer, ForeignKey("customer.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(String(4000))

    menu_item = relationship("MenuItem", back_populates="review")
    customer = relationship("Customer", back_populates="review")

    # orders = relationship("Order", back_populates="customer")
    # review = relationship("Review", back_populates="customer")