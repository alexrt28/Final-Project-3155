from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    payment_type = Column(String(100), nullable=False)
    card_info = Column(String(50), nullable=False)
    status = Column(String(100),nullable=False)

    order = relationship("Order", back_populates="payment")