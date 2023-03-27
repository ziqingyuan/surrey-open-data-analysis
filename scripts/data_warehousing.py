from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql
import os
import sys
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from model import TransitStop, Restaurant


db_user = 'root'
db_pass = 'cpsc-304'
db_host = 'cpsc304.cdj9od1aqevv.us-west-2.rds.amazonaws.com'
db_name = 'cpsc304'

def get_engine():
    """Returns a new SQLAlchemy session, with pymysql engine."""

    engine = create_engine(f'mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}')
    return engine


def reset():
    """ Reset database for transit stop table and restaurant table. """
    conn = pymysql.connect(host=db_host, user=db_user, password=db_pass, db=db_name)

    f = open('../scripts/database_init.sql', 'r')
    sql_script = f.read()

    statements = sql_script.split(';\n\n')
    cursor = conn.cursor()
    for statement in statements:
        if statement.strip() != '':
            cursor.execute(statement)

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()


def transitstop_storing(transit_stop_list: List[TransitStop]):
    """
    Store processed, clean data for transit stop data to mysql db with pymysql engine.
    :param transit_stop_list: TrasitStop array
    :return:
    """
    # TODO: possible to combine with restaurant_storing if abstract data
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    for stop in transit_stop_list:
        session.add(stop)
    session.commit()
    session.close()


def restaurant_storing(restaurant_list: List[Restaurant]):
    """
    Store processed, clean data for restaurant data to mysql db with pymysql engine.
    :param restaurant_list: Restaurant array
    :return:
    """
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    for restaurant in restaurant_list:
        session.add(restaurant)
    session.commit()
    session.close()