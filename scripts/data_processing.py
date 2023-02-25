import json
import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import string
import model
from typing import List, Any
from pyproj import Transformer, Proj, transform
from model import TransitStopRaw, TransitStop


def load_transit_data():
    """
        Load transit_stops object from transit data json file,
        garenteed that the data is an array format with the third element been the transit stop data,
        stops information is stored in the property named "features" of the third element.

        Args:
            none, json file should already been stored in data/raw folder before calling this method

        Returns:
            A python array, each is a transit stop info
    """
    transit_file = open('../data/raw/transit.json')
    transit_data = json.load(transit_file)
    return transit_data[2].get('features')


def get_stop_coordinates(stop: Any):
    """
        Get the coordinate information of a transit stop.

        Args:
            A python object representing a transit stop information

        Returns:
            A python array, represent the coordinated of a transit stop, under standard EPSG:26910
    """
    return stop.get('geometry').get('coordinates')


def get_stop_property(stop: Any, property_name: string):
    """
        Get a specific property information of a transit stop.

        Args:
            A python object representing a transit stop information

        Returns:
            A string/integer represent that piece of property
    """
    return stop.get('properties').get(property_name)


def parse_to_raw_stop_data(transit_stop_array: List[TransitStopRaw]):
    stops_raw_data = load_transit_data()
    for stop in stops_raw_data:
        if "Point" != stop.get('geometry').get('type'):
            continue
        stop_property = stop.get('properties')
        stop_id = stop_property.get('BUS_STOP_NO')
        stop_coordinates = stop.get('geometry').get('coordinates')
        stop_location = stop_property.get('LOCATION')
        stop_x = stop_coordinates[0]
        stop_y = stop_coordinates[1]
        stop_raw = TransitStopRaw(
            id=stop_id,
            location=stop_location,
            x=stop_x,
            y=stop_y
        )
        transit_stop_array.append(stop_raw)


def convert_to_latlon(raw_data_arr: List[TransitStopRaw],
                      parsed_arr: List[TransitStop],
                      lon_arr: List[float],
                      lat_arr: List[float]):
    wgs84_sys = Proj("EPSG:4326")
    utm_surrey_sys = Proj("EPSG:26910")
    for stop_raw in raw_data_arr:
        x = stop_raw.x
        y = stop_raw.y
        lon, lat = transform(utm_surrey_sys, wgs84_sys, x, y)
        lon_arr.append(lon)
        lat_arr.append(lat)
        stop_cleaned = TransitStop(
            id=stop_raw.id,
            location=stop_raw.location,
            lon=lon,
            lat=lat
        )
        parsed_arr.append(stop_cleaned)