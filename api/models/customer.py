from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(20), unique=True, nullable=True)
    address = Column(String(100), nullable=True)

    order = relationship("Order", back_populates="customer")
    review = relationship("Review", back_populates="customer")
