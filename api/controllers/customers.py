from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, Response, status
from ..models import customer as model


def normalize_optional(value):
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return value


def create(db: Session, request):
    name = request.name.strip() if request.name else None
    email = normalize_optional(request.email)
    phone = normalize_optional(request.phone)
    address = normalize_optional(request.address)

    if not name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required.")

    if not request.is_guest and (not email or not phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Non-guest customers need email and phone."
        )

    new_item = model.Customer(
        name=name,
        email=email,
        phone=phone,
        address=address
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all(db: Session):
    try:
        result = db.query(model.Customer).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Customer).filter(model.Customer.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Customer).filter(model.Customer.id == item_id)
        current_item = item.first()
        if not current_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        update_data = request.dict(exclude_unset=True)

        if "name" in update_data:
            update_data["name"] = update_data["name"].strip() if update_data["name"] else None
        if "email" in update_data:
            update_data["email"] = normalize_optional(update_data["email"])
        if "phone" in update_data:
            update_data["phone"] = normalize_optional(update_data["phone"])
        if "address" in update_data:
            update_data["address"] = normalize_optional(update_data["address"])

        name = update_data.get("name", current_item.name)
        email = update_data.get("email", current_item.email)
        phone = update_data.get("phone", current_item.phone)
        is_guest = update_data.get("is_guest", False)

        if not name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required.")

        if not is_guest and (not email or not phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Non-guest customers need email and phone."
            )

        update_data.pop("is_guest", None)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Customer).filter(model.Customer.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
