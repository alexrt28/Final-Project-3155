from decimal import Decimal
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import orders as model
from ..models import customer as customer_model
from ..models import order_item as order_item_model
from ..models import menu_item as menu_item_model


def normalize_optional(value):
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def generate_tracking_number(db: Session):
    while True:
        tracking_number = f"ORD-{uuid4().hex[:10].upper()}"
        existing_item = db.query(model.Order).filter(
            model.Order.tracking_number == tracking_number
        ).first()
        if not existing_item:
            return tracking_number


def create(db: Session, request):
    try:
        if request.order_type not in ["takeout", "delivery"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order type.")

        if not request.items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must include items.")

        delivery_address = normalize_optional(request.delivery_address)

        if request.customer_id:
            customer = db.query(customer_model.Customer).filter(
                customer_model.Customer.id == request.customer_id
            ).first()
            if not customer:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found!")
        else:
            customer_name = request.customer_name.strip() if request.customer_name else None
            customer_email = normalize_optional(request.customer_email)
            customer_phone = normalize_optional(request.customer_phone)

            if not customer_name:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer name is required.")

            if not request.is_guest and (not customer_email or not customer_phone):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Non-guest orders need customer email and phone."
                )

            customer = customer_model.Customer(
                name=customer_name,
                email=customer_email,
                phone=customer_phone,
                address=delivery_address
            )
            db.add(customer)
            db.flush()

        if request.order_type == "delivery":
            if delivery_address:
                customer.address = delivery_address
            if not customer.address:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Delivery orders need an address."
                )

        new_item = model.Order(
            customer_id=customer.id,
            promo_code_id=request.promo_code_id,
            order_type=request.order_type,
            tracking_number=generate_tracking_number(db),
            status=request.status or "pending",
            total_price=Decimal("0.00")
        )

        db.add(new_item)
        db.flush()

        total_price = Decimal("0.00")
        for order_detail in request.items:
            if order_detail.quantity <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than 0.")

            menu_item = db.query(menu_item_model.MenuItem).filter(
                menu_item_model.MenuItem.id == order_detail.menu_item_id
            ).first()
            if not menu_item:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")

            subtotal = Decimal(str(menu_item.price)) * order_detail.quantity
            total_price += subtotal

            new_order_detail = order_item_model.OrderItem(
                order_id=new_item.id,
                menu_item_id=order_detail.menu_item_id,
                quantity=order_detail.quantity,
                subtotal=subtotal
            )
            db.add(new_order_detail)

        new_item.total_price = total_price
        db.commit()
        db.refresh(new_item)
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def read_by_tracking(db: Session, tracking_number):
    try:
        item = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking number not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        current_item = item.first()
        if not current_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        update_data = request.dict(exclude_unset=True)
        delivery_address = normalize_optional(update_data.pop("delivery_address", None))

        if "order_type" in update_data and update_data["order_type"] not in ["takeout", "delivery"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order type.")

        if delivery_address and current_item.customer:
            current_item.customer.address = delivery_address

        next_order_type = update_data.get("order_type", current_item.order_type)
        next_address = current_item.customer.address if current_item.customer else None
        if next_order_type == "delivery" and not next_address:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivery orders need an address."
            )

        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        db.query(order_item_model.OrderItem).filter(
            order_item_model.OrderItem.order_id == item_id
        ).delete(synchronize_session=False)
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
