from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base, engine

class PointOfSale(Base):
    __tablename__ = "points_of_sale"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    city_id = Column(Integer)
    phone = Column(String(20))
    email = Column(String(100))
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)