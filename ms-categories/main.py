from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine
from models import Category
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse
from utils import get_db
from auth import verify_admin_role

app = FastAPI(title="MS Categories")


Base.metadata.create_all(bind=engine)


# Endpoints

@app.get("/categories", response_model=list[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@app.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(404, "La categoría no existe.")
    return category


@app.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=201,
    dependencies=[Depends(verify_admin_role)]
)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.put(
    "/categories/{category_id}",
    response_model=CategoryResponse,
    dependencies=[Depends(verify_admin_role)]
)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(404, "La categoría no existe.")

    for key, value in category.model_dump().items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete(
    "/categories/{category_id}",
    status_code=204,
    dependencies=[Depends(verify_admin_role)]
)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(404, "La categoría no existe.")

    db.delete(db_category)
    db.commit()
    return None