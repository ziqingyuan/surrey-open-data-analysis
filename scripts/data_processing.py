import csv
import json
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import string
import pandas as pd
from typing import List, Any
import pyproj
from model import TransitStop, Restaurant


DATA_PATH = "../data/"

class GeoSystem:
    """
    A class representing static geological system name.

    Attributes:
    - WGS84: Name of Lat-Lon system
    - UTM_SURREY: Name of UTM system for the UTM block Surrey is in
    """
    WGS84 = "EPSG:4326"
    UTM_SURREY = "EPSG:26910"


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
    transit_file = open(DATA_PATH + 'raw/transit.json')
    transit_data = json.load(transit_file)
    return transit_data[2].get('features')


def get_stop_coordinates(stop: Any):
    """
    Get the coordinate information of a transit stop.
    :param stop: A python object representing a transit stop information
    :return: A python array, represent the coordinated of a transit stop, under standard EPSG:26910
    """
    return stop.get('geometry').get('coordinates')


def get_stop_property(stop: Any, property_name: string):
    """
    Get a specific property information of a transit stop.
    :param stop: A python object representing a transit stop information
    :param property_name: A string/integer represent that piece of property
    :return:
    """
    return stop.get('properties').get(property_name)


def json_to_stop_data(transit_stop_array: List[TransitStop]):
    """
    Higher level function for converting json file and storing parsed data into the input array.
    :param transit_stop_array: An array to storing the parsed transit stop instances.
    :return:
    """
    stops_raw_data = load_transit_data()
    for stop in stops_raw_data:
        if "Point" != stop.get('geometry').get('type'):
            continue
        stop_property = stop.get('properties')
        stop_id = stop_property.get('BUS_STOP_NO')
        stop_coordinates = stop.get('geometry').get('coordinates')
        stop_location = stop_property.get('LOCATION')
        stop_name = stop_location if not stop_location.isupper() else ""
        stop_city = stop_location if stop_location.isupper() else "SURREY"
        stop_x = stop_coordinates[0]
        stop_y = stop_coordinates[1]
        lat, lon = map_system_converter(GeoSystem.UTM_SURREY, GeoSystem.WGS84, stop_x, stop_y)
        stop_raw = TransitStop(
            id=stop_id,
            city=stop_city,
            name=stop_name,
            utm_x=stop_x,
            utm_y=stop_y,
            lon=lon,
            lat=lat

        )
        transit_stop_array.append(stop_raw)


def create_restaurant(row):
    """ Convert a row in original csv file to a restaurant object."""
    tracking_number = row[0]
    name = row[1]
    city = row[2]
    address = row[3]
    lon = row[4]
    lat = row[5]
    x, y = map_system_converter(GeoSystem.WGS84, GeoSystem.UTM_SURREY, lat, lon)
    new_restaurant = Restaurant(
        tracking_number=tracking_number,
        name=name,
        city=city,
        address=address,
        lon=lon,
        lat=lat,
        utm_x=x,
        utm_y=y)
    return new_restaurant


def csv_to_restaurant_data(restaurant_array: List[Restaurant]):
    """
    Higher level function for converting csv file and storing parsed data into the input array.
    :param restaurant_array: An array to storing the parsed restaurant instances.
    :return:
    """
    restaurant_data = pd.read_table(DATA_PATH + "raw/restaurants.csv", sep=',')
    zip_data = zip(restaurant_data['TRACKINGNUMBER'],
                   restaurant_data['NAME'],
                   restaurant_data['PHYSICALCITY'],
                   restaurant_data['PHYSICALADDRESS'],
                   restaurant_data['LONGITUDE'],
                   restaurant_data['LATITUDE'])
    for row in zip_data:
        restaurant_array.append(create_restaurant(row))


def map_system_converter(orig_sys: string, to_sys: string, x: float, y: float):
    """
    Covert a geological coordinate from original system to target system

    :param orig_sys: a string represent original system name
    :param to_sys: a string represent target system name
    :param x: the first value in the coordinate, longitude for lon-lat system, x for utm system
    :param y: the second value in the coordinate, latitude for lon-lat system, y for utm system
    :return: A tuple of float depend on the target system
    """
    transformer = pyproj.Transformer.from_crs(orig_sys, to_sys)

    x_after, y_after = transformer.transform(x, y)
    return x_after, y_after


def generate_clean_restaurant(restaurant_array: List[Restaurant]):
    """
    Store the processed data into csv file.
    :param restaurant_array: array of processed restaurant.
    :return:
    """
    # Define the fieldnames for the CSV file
    fieldnames = ["TRACKINGNUMBER", "NAME", "CITY", "ADDRESS", "LONGITUDE", "LATITUDE", "UTMX", "UTMY"]

    # Create a new CSV file in write mode
    with open(DATA_PATH + "processed/restaurant.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row to the CSV file
        writer.writeheader()

        # Write each person as a row in the CSV file
        for restaurant in restaurant_array:
            writer.writerow({
                "TRACKINGNUMBER": restaurant.tracking_number,
                "NAME": restaurant.name,
                "CITY": restaurant.city,
                "ADDRESS": restaurant.address,
                "LONGITUDE": restaurant.lon,
                "LATITUDE": restaurant.lat,
                "UTMX": restaurant.utm_x,
                "UTMY": restaurant.utm_y
            })


def generate_clean_transit_stop(transit_stop_array: List[TransitStop]):
    """
    Store the processed data into csv file.
    :param transit_stop_array: array of processed transit stop objects.
    :return:
    """
    # Define the fieldnames for the CSV file
    fieldnames = ["ID", "NAME", "CITY", "LONGITUDE", "LATITUDE", "UTMX", "UTMY"]

    # Create a new CSV file in write mode
    with open(DATA_PATH + "processed/transit_stops.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row to the CSV file
        writer.writeheader()

        # Write each person as a row in the CSV file
        for transit_stop in transit_stop_array:
            writer.writerow({
                "ID": transit_stop.id,
                "NAME": transit_stop.name,
                "CITY": transit_stop.city,
                "LONGITUDE": transit_stop.lon,
                "LATITUDE": transit_stop.lat,
                "UTMX": transit_stop.utm_x,
                "UTMY": transit_stop.utm_y
            })
