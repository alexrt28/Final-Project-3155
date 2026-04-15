from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    order_detail_id =
    payment_id =
    promo_code_id =
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    tracking_number = Column(String(100), unique=True, nullable=False)
    status = Column(String(100), nullable=False)
    total_price = Column(Integer, nullable=False)

    customer = relationship("Customer", back_populates="orders")
