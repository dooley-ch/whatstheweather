# *******************************************************************************************
#  File:  data.py
#
#  Created: 25-08-2022
#
#  History:
#  25-08-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['get_location_record', 'insert_location_record', 'update_location_record',
           'delete_location_record', 'all_locations']

import sqlite3
from pathlib import Path
from loguru import logger
from . import errors
from . import model
from . import utils


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def _init_database(db_con: sqlite3.Connection) -> None:
    sql = """
        CREATE TABLE location(
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            latitude TEXT NOT NULL,
            longitude TEXT NOT NULL,
            timezone TEXT NOT NULL,
            region TEXT,
            country_code TEXT NOT NULL,
            country TEXT,
            post_codes TEXT,
            lock_version INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(name));"""

    try:
        with db_con:
            cursor = db_con.cursor()
            cursor.execute(sql)
    except Exception as e:
        logger.error(f"Failed to create the application database: {e}")
        raise


def _get_connection(file: Path | None = None) -> sqlite3.Connection:
    """
    This function gets the database connection
    """
    if file is None:
        file = utils.app_folder().joinpath("data.sqlite")

    init = False
    if not file.exists():
        init = True

    db_con = sqlite3.connect(file)
    db_con.row_factory = sqlite3.Row

    if init:
        _init_database(db_con)

    return db_con


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def insert_location_record(record: model.Location, file: Path | None = None) -> bool:
    """
    This function inserts a record in the database
    """
    sql = """INSERT INTO location(name, location, latitude, longitude, timezone, region, 
                                    country_code, country, post_codes) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    con = _get_connection(file)

    try:
        with con:
            cursor = con.cursor()
            cursor.execute(sql, (record.name, record.location, record.latitude, record.longitude, record.timezone,
                                 record.region, record.country_code, record.country, ''.join(record.post_codes)))
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        logger.error(f"Failed to insert record: {record.name} - {e}")
        raise
    else:
        return cursor.lastrowid > 0
    finally:
        con.close()


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def delete_location_record(name: str, file: Path | None = None) -> bool:
    """
    This function deletes a database record
    """
    sql = """DELETE FROM location WHERE (name = ?);"""

    con = _get_connection(file)

    try:
        with con:
            cursor = con.cursor()
            cursor.execute(sql, (name,))
        return cursor.rowcount == 1
    except Exception as e:
        logger.error(f"Failed to delete record: {name} - {e}")

    finally:
        con.close()


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def get_location_record(name: str, file: Path | None = None) -> model.Location | None:
    """
    Gets the location record for a given name
    """
    sql = """SELECT name, location, latitude, longitude, region, country_code, country, timezone, post_codes 
                 FROM location WHERE (name = ?)"""

    con = _get_connection(file)

    try:
        cursor = con.cursor()
        cursor.execute(sql, (name,))
        row = cursor.fetchone()
        if row:
            return model.Location(*row)
    except Exception as e:
        logger.error(f"Failed to get location record: {name} - {e}")
        raise
    finally:
        con.close()


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def all_locations(file: Path | None = None) -> model.Locations | None:
    """
    This function returns all the location records in the database
    """
    sql = """SELECT name, location, latitude, longitude, region, country_code, country, timezone, post_codes, 
                lock_version, created_at, updated_at FROM location ORDER BY location"""

    con = _get_connection(file)

    try:
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows:
            records = model.Locations()
            for row in rows:
                records.append(model.Location(*row))
            return records
    except Exception as e:
        logger.error(f"Failed to get location records - {e}")
        raise
    finally:
        con.close()
