from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import menu_item as menu_item_model
from ..models import order_item as model
from ..models import orders as order_model


def recalculate_total(db: Session, order_id):
    order = db.query(order_model.Order).filter(order_model.Order.id == order_id).first()
    if order:
        total = Decimal("0.00")
        for order_item in order.order_items:
            total += Decimal(str(order_item.subtotal))
        order.total_price = total


def create(db: Session, request):
    try:
        order = db.query(order_model.Order).filter(order_model.Order.id == request.order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")

        menu_item = db.query(menu_item_model.MenuItem).filter(
            menu_item_model.MenuItem.id == request.menu_item_id
        ).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")

        if request.quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than 0.")

        new_item = model.OrderItem(
            order_id=request.order_id,
            menu_item_id=request.menu_item_id,
            quantity=request.quantity,
            subtotal=Decimal(str(menu_item.price)) * request.quantity
        )

        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        recalculate_total(db, request.order_id)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.OrderItem).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.OrderItem).filter(model.OrderItem.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.OrderItem).filter(model.OrderItem.id == item_id)
        current_item = item.first()
        if not current_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        update_data = request.dict(exclude_unset=True)
        quantity = update_data.get("quantity", current_item.quantity)
        menu_item_id = update_data.get("menu_item_id", current_item.menu_item_id)

        if quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity must be greater than 0.")

        menu_item = db.query(menu_item_model.MenuItem).filter(
            menu_item_model.MenuItem.id == menu_item_id
        ).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found!")

        update_data["subtotal"] = Decimal(str(menu_item.price)) * quantity
        item.update(update_data, synchronize_session=False)
        db.commit()
        recalculate_total(db, item.first().order_id)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.OrderItem).filter(model.OrderItem.id == item_id)
        current_item = item.first()
        if not current_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        order_id = current_item.order_id
        item.delete(synchronize_session=False)
        db.commit()
        recalculate_total(db, order_id)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
