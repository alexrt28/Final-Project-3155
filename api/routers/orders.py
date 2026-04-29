from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/tracking/{tracking_number}", response_model=schema.Order)
def read_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    return controller.read_by_tracking(db, tracking_number=tracking_number)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.get("/revenue/{target_date}")
def get_daily_revenue(target_date: date, db: Session = Depends(get_db)):
    results = controller.get_daily_revenue(db, target_date)
    if results["total_revenue"] in None or results["total_revenue"] == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No orders found for {target_date}"
        )
    return results

@router.get("/range/")
def get_orders_range(start_date: date, end_date: date, db: Session = Depends(get_db)):

    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date."
        )

    orders = controller.get_orders_by_date_range(db, start_date, end_date)

    if not orders:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No orders found for range between {start_date} and {end_date}"
        )
    return orders