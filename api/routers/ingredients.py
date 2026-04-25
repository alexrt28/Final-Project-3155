from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies.database import get_db
from ..schemas import ingredient as schema
from ..controllers import ingredients as controller


router = APIRouter(
    tags=["ingredients"],
    prefix="/ingredients"
)

@router.post("/", response_model=schema.Ingredient)
def create(request: schema.IngredientCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Ingredient])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schema.Ingredient)
def get_ingredient(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, item_id=item_id)

@router.put("/{item_id}", response_model=schema.Ingredient)
def update_ingredient(item_id: int, request: schema.IngredientUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, item_id=item_id, request=request)

@router.delete("/{item_id}}")
def delete_ingredient(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)