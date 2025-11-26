from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db, engine
from models import PointOfSale, Base
from schemas import PointOfSaleCreate, PointOfSaleUpdate, PointOfSaleResponse
from auth import verify_admin_role
from city_client import verify_city_exists
import asyncio

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Points of Sale Microservice",
    description="Microservicio para gestionar puntos de venta",
    version="1.0.0"
)


@app.post("/points-of-sale", response_model=PointOfSaleResponse, status_code=status.HTTP_201_CREATED)
async def create_point_of_sale(
    pos: PointOfSaleCreate,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(verify_admin_role)
):

    if not pos.name or not pos.address or not pos.city_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los campos name, address y city_id son requeridos"
        )

    if pos.name.strip() == "" or pos.address.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name y address no pueden estar vacíos"
        )


    await verify_city_exists(pos.city_id)

    existing_pos = db.query(PointOfSale).filter(PointOfSale.name == pos.name).first()
    if existing_pos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un punto de venta con ese nombre"
        )

    db_pos = PointOfSale(
        name=pos.name,
        address=pos.address,
        city_id=pos.city_id,
        phone=pos.phone,
        email=pos.email,
        is_active=pos.is_active
    )

    try:
        db.add(db_pos)
        db.commit()
        db.refresh(db_pos)
        return db_pos
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear el punto de venta"
        )

@app.get("/points-of-sale", response_model=List[PointOfSaleResponse])
def get_points_of_sale(
        skip: int = 0,
        limit: int = 100,
        city_id: int = None,
        db: Session = Depends(get_db)
):
    query = db.query(PointOfSale).filter(PointOfSale.is_active == 1)

    if city_id:
        query = query.filter(PointOfSale.city_id == city_id)

    points_of_sale = query.offset(skip).limit(limit).all()
    return points_of_sale


@app.get("/points-of-sale/{pos_id}", response_model=PointOfSaleResponse)
def get_point_of_sale(
        pos_id: int,
        db: Session = Depends(get_db)
):
    pos = db.query(PointOfSale).filter(PointOfSale.id == pos_id, PointOfSale.is_active == 1).first()
    if not pos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de venta no encontrado"
        )
    return pos


@app.put("/points-of-sale/{pos_id}", response_model=PointOfSaleResponse)
async def update_point_of_sale(
        pos_id: int,
        pos: PointOfSaleUpdate,
        db: Session = Depends(get_db),
        is_admin: bool = Depends(verify_admin_role)
):

    if not pos.name or not pos.address or not pos.city_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los campos name, address y city_id son requeridos"
        )

    await verify_city_exists(pos.city_id)

    if pos.name.strip() == "" or pos.address.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name y address no pueden estar vacíos"
        )

    db_pos = db.query(PointOfSale).filter(PointOfSale.id == pos_id).first()
    if not db_pos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de venta no encontrado"
        )


    if pos.name != db_pos.name:
        existing_pos = db.query(PointOfSale).filter(PointOfSale.name == pos.name, PointOfSale.id != pos_id).first()
        if existing_pos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otro punto de venta con ese nombre"
            )

    try:
        db_pos.name = pos.name
        db_pos.address = pos.address
        db_pos.city_id = pos.city_id
        db_pos.phone = pos.phone
        db_pos.email = pos.email
        db_pos.is_active = pos.is_active

        db.commit()
        db.refresh(db_pos)
        return db_pos
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar el punto de venta"
        )


@app.delete("/points-of-sale/{pos_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_point_of_sale(
        pos_id: int,
        db: Session = Depends(get_db),
        is_admin: bool = Depends(verify_admin_role)
):
    db_pos = db.query(PointOfSale).filter(PointOfSale.id == pos_id).first()
    if not db_pos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Punto de venta no encontrado"
        )

    try:
        db.delete(db_pos)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al eliminar el punto de venta"
        )


@app.get("/")
def read_root():
    return {"message": "Microservicio de Puntos de Venta funcionando correctamente"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8003)