from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import recipes as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_item = model.Recipe(
        amount = request.amount,
        unit = request.unit,
        menu_item_id = request.menu_item_id,
        ingredient_id = request.ingredient_id
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as exception:
        error = str(exception.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item

def read_all(db: Session):
    try:
        result = db.query(model.Recipe).all()
    except SQLAlchemyError as exception:
        error = str(exception.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Recipe).filter(model.Recipe.id == item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    except SQLAlchemyError as exception:
        error = str(exception.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, item_id: int, request):
    try:
        item = db.query(model.Recipe).filter(model.Recipe.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as exception:
        error = str(exception.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

def delete(db: Session, item_id):
    try:
        item = db.query(model.Recipe).filter(model.Recipe.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as exception:
        error = str(exception.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)