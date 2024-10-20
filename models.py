from sqlalchemy import Column, Integer, String, LargeBinary, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    location_name = Column(String)
    food_item = Column(String)
    since_when = Column(String)
    till_when = Column(String)
    veg_nonveg = Column(String)
    requirements = Column(String)
    picture = Column(LargeBinary)  # If pictures are stored as binary
    lat = Column(Float)
    lon = Column(Float)
