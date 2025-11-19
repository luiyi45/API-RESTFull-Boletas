from pydantic import BaseModel

class CityBase(BaseModel):
    name: str
    country: str
    is_active: int = 1

class CityCreate(CityBase):
    pass

class CityUpdate(CityBase):
    pass

class CityResponse(CityBase):
    id: int

    class Config:
        from_attributes = True