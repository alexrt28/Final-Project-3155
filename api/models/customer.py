from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # removed: review_id = Column(Integer, ForeignKey("review.id"))
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    address = Column(String(100), nullable=False)

    order = relationship("Order", back_populates="customer")
    review = relationship("Review", back_populates="customer")