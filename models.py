# models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, LargeBinary

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    food_item = Column(String(100), nullable=False)
    since_when = Column(String(10), nullable=False)
    till_when = Column(String(10), nullable=False)
    veg_nonveg = Column(String(10), nullable=False)
    requirements = Column(Text, nullable=True)
    lat = Column(String(20), nullable=False)
    lon = Column(String(20), nullable=False)
    picture = Column(LargeBinary, nullable=True)
    location_name = Column(String(200), nullable=False)