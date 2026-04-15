from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    customer_id = Column(Integer, ForeignKey("customer.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(String(4000))

    orders = relationship("Customer", back_populates="review")

    # orders = relationship("Order", back_populates="customer")
    # review = relationship("Review", back_populates="customer")