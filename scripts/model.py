from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TransitStopRaw:
    def __init__(self, id, x, y, location):
        self.id = id
        self.x = x
        self.y = y
        self.location = location


class TransitStop(Base):
    __tablename__ = 'transit_stops'

    id = Column(Integer, primary_key=True)
    lon = Column(Float)
    lat = Column(Float)
    location = Column(String)

    def __init__(self, id, lon, lat, location):
        self.id = id
        self.lon = lon
        self.lat = lat
        self.location = location


class Restaurant(Base):
    __tablename__ = 'transit_stops'

    id = Column(Integer, primary_key=True)
    lon = Column(Float)
    lat = Column(Float)
    location = Column(String)

    def __init__(self, id, lon, lat, location):
        self.id = id
        self.lon = lon
        self.lat = lat
        self.location = location