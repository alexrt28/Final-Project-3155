from fastapi import APIRouter, Depends, FastAPI, status, Response, HTTPException
from sqlalchemy.orm import Session
from ..controllers import menu_item as controller
from ..schemas import menu_item as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Menu Items'],
    prefix="/menu_items"
)

@router.post("/", response_model=schema.MenuItem)
def create(request: schema.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.MenuItem])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/search/")
def search_menu(category: str, db: Session = Depends(get_db)):
    results = controller.search_by_category(db, category)
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No menu items found for category/search: '{category}"
        )
    return results

@router.get("/{item_id}", response_model=schema.MenuItem)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.MenuItem)
def update(item_id: int, request: schema.MenuItemUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)