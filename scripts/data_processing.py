import json
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import string
import model
from typing import List

from model import TransitStopRaw


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


def get_stop_coordinates(stop):
    """
        Get the coordinate information of a transit stop.

        Args:
            A python object representing a transit stop information

        Returns:
            A python array, represent the coordinated of a transit stop, under standard EPSG:26910
    """
    return stop.get('geometry').get('coordinates')


def get_stop_property(stop, property_name):
    """
        Get a specific property information of a transit stop.

        Args:
            A python object representing a transit stop information

        Returns:
            A string/integer represent that piece of property
    """
    return stop.get('properties').get(property_name)


def parse_to_raw_stop_data(transit_stop_array):
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

