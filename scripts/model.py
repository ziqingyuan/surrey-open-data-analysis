from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TransitStop(Base):
    """
            A class representing a TransitStop.

            Attributes:
            - id (str): The BUS_STOP_NO
            - name (str): The bus stop's name (if provided)
            - lon (float): The bus stop's longitude
            - lat (float): The bus stop's latitude
            - location (str): The bus stop's belonging city
            - utm_x (float): The bus stop's coordinates under UTM system
            - utm_y (float): The bus stop's coordinates under UTM system
    """
    __tablename__ = 'transit_stop'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    lon = Column(Float)
    lat = Column(Float)
    city = Column(String)
    utm_x = Column(Float)
    utm_y = Column(Float)

    def __init__(self, id, lon, lat, city, name, utm_x, utm_y):
        self.id = id
        self.lon = lon
        self.lat = lat
        self.city = city
        self.name = name
        self.utm_x = utm_x
        self.utm_y = utm_y


class Restaurant(Base):
    """
            A class representing a Restaurant.

            Attributes:
            - tracking_number (str): The restaurant's primary id
            - lon (float): The restaurant's longitude
            - lat (float): The restaurant's latitude
            - location (str): The restaurant's address
            - utm_x (float): The restaurant's coordinates under UTM system
            - utm_y (float): The restaurant's coordinates under UTM system
    """

    __tablename__ = 'restaurant'

    tracking_number = Column(String, primary_key=True)
    lon = Column(Float)
    lat = Column(Float)
    name = Column(String)
    city = Column(String)
    address = Column(String)
    utm_x = Column(Float)
    utm_y = Column(Float)

    def __init__(self, tracking_number, name, lon, lat, city, address, utm_x, utm_y):
        self.tracking_number = tracking_number
        self.name = name
        self.lon = lon
        self.lat = lat
        self.city = city
        self.address = address
        self.utm_x = utm_x
        self.utm_y = utm_y



