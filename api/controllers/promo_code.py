from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status, Response
from ..models import promo_code as model


def create(db: Session, request):
    new_promo = model.PromoCode(
        promo_code = request.code.upper(),
        discount = request.discount,
        discount_type = request.discount_type,
        expiry = request.expiry
    )

    try:
        db.add(new_promo)
        db.commit()
        db.refresh(new_promo)
    except SQLAlchemyError as exception:
        error = str(exception.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_promo

def read_all(db: Session):
    try:
        result = db.query(model.PromoCode).all()
    except SQLAlchemyError as exception:
        error = str(exception.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id):
    try:
        item = db.query(model.PromoCode).filter(model.PromoCode.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found')
        return item
    except SQLAlchemyError as exception:
        error = str(exception.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def update(db: Session, item_id, request):
    try:
        item = db.query(model.PromoCode).filter(model.PromoCode.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found')
        update_data = request.dict(exclude_unset = True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as exception:
        error = str(exception.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def delete(db: Session, item_id):
    try:
        query = db.query(model.PromoCode).filter(model.PromoCode.id == item_id)
        if not query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID not found')
        query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as exception:
        error = str(exception.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)