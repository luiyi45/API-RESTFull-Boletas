from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import secrets

from database import get_db, engine
from models import User, Base
from schemas import UserCreate, UserLogin, UserResponse, Token
from auth import get_current_user, verify_admin_role
from utils import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication Microservice",
    description="Microservicio para autenticación y gestión de usuarios",
    version="1.0.0"
)



@app.on_event("startup")
def create_default_admin():
    db = next(get_db())
    try:
        admin_user = db.query(User).filter(User.email == "admin@eventos.com").first()
        if not admin_user:
            hashed_password = get_password_hash("admin123")
            admin_user = User(
                name="Administrador",
                email="admin@eventos.com",
                password=hashed_password,
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            print("Usuario admin creado: admin@eventos.com / admin123")
    except Exception as e:
        print(f"Error creando admin: {e}")
    finally:
        db.close()


@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):


    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )


    hashed_password = get_password_hash(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al registrar el usuario"
        )


@app.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login_user(
        user_data: UserLogin,
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Crear token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@app.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_current_user_info(
        current_user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user


@app.get("/users", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(
        current_user: dict = Depends(verify_admin_role),
        db: Session = Depends(get_db)
):

    users = db.query(User).all()
    return users


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: int,
        current_user: dict = Depends(verify_admin_role),
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )


    if user.email == current_user["email"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes eliminar tu propio usuario"
        )

    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al eliminar el usuario"
        )


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():

    return {"message": "Microservicio de Autenticación funcionando correctamente"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)