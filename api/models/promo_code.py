from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class PromoCode(Base):
    __tablename__ = "promo_code"

    code = Column(Integer, primary_key=True, index=True, autoincrement=True)
    discount = Column(Integer, nullable=False)
    expiry = Column(DATETIME, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))

    order = relationship("Order", back_populates="promo_code")