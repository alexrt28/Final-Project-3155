from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    customer_id = Column(Integer, ForeignKey("customer.id"))
    # removed: order_item_id = Column(Integer, ForeignKey("order_item.id"))
    # removed: payment_id = Column(Integer, ForeignKey("payment.id"))
    promo_code_id = Column(Integer, ForeignKey("promo_code.id"))

    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    tracking_number = Column(String(100), unique=True, nullable=False)
    status = Column(String(100), nullable=False)
    total_price = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="order")
    order_items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order")
    promo_code = relationship("PromoCode", back_populates="order")