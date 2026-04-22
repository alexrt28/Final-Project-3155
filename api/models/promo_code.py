from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class PromoCode(Base):
    __tablename__ = "promo_code"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # removed: order_id = Column(Integer, ForeignKey("orders.id"))
    promo_code = Column(String(12), unique=True, nullable=False)
    discount = Column(Integer, nullable=False)
    discount_type = Column(String)  # % off? flat $ off?
    expiry = Column(DATETIME, nullable=False)

    order = relationship("Order", back_populates="promo_code")