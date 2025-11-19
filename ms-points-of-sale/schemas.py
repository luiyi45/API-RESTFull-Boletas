from pydantic import BaseModel, EmailStr
from typing import Optional

class PointOfSaleBase(BaseModel):
    name: str
    address: str
    city_id: int
    phone: Optional[str]
    email: Optional[str]
    is_active: int = 1

class PointOfSaleCreate(PointOfSaleBase):
    pass

class PointOfSaleUpdate(PointOfSaleBase):
    pass

class PointOfSaleResponse(PointOfSaleBase):
    id: int

    class Config:
        from_attributes = True