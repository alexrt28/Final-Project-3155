from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from ..models import review as model
from ..models import menu_item


def create(db: Session, request):
    new_review = model.Review(
        customer_id=request.customer_id,
        menu_item_id=request.menu_item_id,
        rating=request.rating,
        comment=request.comment
    )

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_review


def read_all(db: Session):
    return db.query(model.Review).all()


def read_one(db: Session, review_id: int):
    review = db.query(model.Review).filter(model.Review.id == review_id).first()

    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    return review


def update(db: Session, review_id: int, request):
    review_query = db.query(model.Review).filter(model.Review.id == review_id)

    if not review_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    try:
        review_query.update(request.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return review_query.first()


def delete(db: Session, review_id: int):
    review_query = db.query(model.Review).filter(model.Review.id == review_id)

    if not review_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    review_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def analytics(db: Session):
    results = (
        db.query(
            menu_item.MenuItem.id.label("menu_item_id"),
            menu_item.MenuItem.name.label("menu_item_name"),
            func.avg(model.Review.rating).label("average_rating"),
            func.count(model.Review.id).label("total_reviews")
        )
        .join(menu_item.MenuItem, model.Review.menu_item_id == menu_item.MenuItem.id)
        .group_by(menu_item.MenuItem.id, menu_item.MenuItem.name)
        .order_by(func.avg(model.Review.rating).asc())
        .all()
    )

    return [
        {
            "menu_item_id": row.menu_item_id,
            "menu_item_name": row.menu_item_name,
            "average_rating": round(float(row.average_rating), 2),
            "total_reviews": row.total_reviews,
            "quality_status": "Unpopular dish" if float(row.average_rating) < 3 else "Good"
        }
        for row in results
    ]


def dissatisfaction_reasons(db: Session):
    bad_reviews = (
        db.query(
            menu_item.MenuItem.name.label("menu_item_name"),
            model.Review.rating,
            model.Review.comment
        )
        .join(menu_item.MenuItem, model.Review.menu_item_id == menu_item.MenuItem.id)
        .filter(model.Review.rating <= 2)
        .all()
    )

    return [
        {
            "menu_item_name": row.menu_item_name,
            "rating": row.rating,
            "reason": row.comment
        }
        for row in bad_reviews
    ]