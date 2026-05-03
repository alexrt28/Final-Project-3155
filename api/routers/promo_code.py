from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..controllers import promo_code as controller
from ..schemas import promo_code as schema
from ..dependencies.database import get_db


router = APIRouter(
    tags=['Promo Codes'],
    prefix="/promo-codes"
)

@router.post("/", response_model=schema.PromoCode)
def create_promo_code(request: schema.PromoCodeCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.PromoCode])
def read_all_promo_codes(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.PromoCode)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id = item_id)

@router.put("/{item_id}", response_model=schema.PromoCode)
def update(item_id: int, request: schema.PromoCodeUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.get("/apply/{code}")
def apply_promo(code: str, total: float, db: Session = Depends(get_db)):
    final_price = controller.apply_and_validate_code(db, code, total)
    return {"final_price": round(final_price, 2)}