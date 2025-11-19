from sqlalchemy import Column, Integer, String
from database import Base, engine


class City(Base):

    __tablename__ = "cities"


    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, index=True, nullable=False)

    country = Column(String(100), nullable=False)

    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive


def create_tables():

    Base.metadata.create_all(bind=engine)