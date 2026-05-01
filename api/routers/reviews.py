from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import reviews as controller
from ..schemas import review as schema
from ..dependencies.database import get_db


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


@router.post("/", response_model=schema.Review)
def create_review(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Review])
def get_all_reviews(db: Session = Depends(get_db)):
    return controller.read_all(db=db)


@router.get("/analytics")
def get_review_analytics(db: Session = Depends(get_db)):
    return controller.analytics(db=db)


@router.get("/dissatisfaction")
def get_dissatisfaction_reasons(db: Session = Depends(get_db)):
    return controller.dissatisfaction_reasons(db=db)


@router.get("/{review_id}", response_model=schema.Review)
def get_one_review(review_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, review_id=review_id)


@router.put("/{review_id}", response_model=schema.Review)
def update_review(review_id: int, request: schema.ReviewUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, review_id=review_id, request=request)


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, review_id=review_id)