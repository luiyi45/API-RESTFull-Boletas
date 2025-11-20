from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db, engine
from models import City, create_tables
from schemas import CityCreate, CityUpdate, CityResponse
from auth import verify_admin_role

# Create tables on startup
create_tables()

app = FastAPI(
    title="Cities Microservice",
    description="Microservicio para gestionar ciudades",
    version="1.0.0"
)


@app.post("/cities", response_model=CityResponse, status_code=status.HTTP_201_CREATED)
def create_city(
        city: CityCreate,
        db: Session = Depends(get_db),
        is_admin: bool = Depends(verify_admin_role)
):

    if not city.name or not city.country:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los campos name y country son requeridos"
        )


    if city.name.strip() == "" or city.country.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name y country no pueden estar vacíos"
        )

    existing_city = db.query(City).filter(City.name == city.name).first()
    if existing_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una ciudad con ese nombre"
        )

    db_city = City(
        name=city.name,
        country=city.country,
        is_active=city.is_active
    )

    try:
        db.add(db_city)
        db.commit()
        db.refresh(db_city)
        return db_city
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear la ciudad"
        )


@app.get("/cities", response_model=List[CityResponse])
def get_cities(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    cities = db.query(City).filter(City.is_active == 1).offset(skip).limit(limit).all()
    return cities


@app.get("/cities/{city_id}", response_model=CityResponse)
def get_city(
        city_id: int,
        db: Session = Depends(get_db)
):
    city = db.query(City).filter(City.id == city_id, City.is_active == 1).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada"
        )
    return city


@app.put("/cities/{city_id}", response_model=CityResponse)
def update_city(
        city_id: int,
        city: CityUpdate,
        db: Session = Depends(get_db),
        is_admin: bool = Depends(verify_admin_role)
):

    if not city.name or not city.country:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los campos name y country son requeridos"
        )


    if city.name.strip() == "" or city.country.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name y country no pueden estar vacíos"
        )

    db_city = db.query(City).filter(City.id == city_id).first()
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada"
        )

    if city.name != db_city.name:
        existing_city = db.query(City).filter(City.name == city.name, City.id != city_id).first()
        if existing_city:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe otra ciudad con ese nombre"
            )

    try:
        db_city.name = city.name
        db_city.country = city.country
        db_city.is_active = city.is_active

        db.commit()
        db.refresh(db_city)
        return db_city
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al actualizar la ciudad"
        )


@app.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db),
        is_admin: bool = Depends(verify_admin_role)
):
    db_city = db.query(City).filter(City.id == city_id).first()
    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad no encontrada"
        )

    try:
        db.delete(db_city)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al eliminar la ciudad"
        )


@app.get("/")
def read_root():
    return {"message": "Microservicio de Ciudades funcionando correctamente"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)