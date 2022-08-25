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

__all__ = ['insert_location', 'update_location', 'delete_location', 'all_locations']

from typing import Any
import sqlite3
from pathlib import Path
import attrs
from . support import app_folder
from . model import Location, LocationRecord, LocationRecordMetadata, Locations
from . errors import DuplicateRecordError, RecordNotFoundError


def _filter(field: attrs.Attribute, value: Any) -> bool:
    """
    This function filters the attrs asdict function to only return values
    needed to insert a new record
    """
    field_name = field.name
    if field_name in ['lock_version', 'created_at', 'updated_at']:
        return False

    return True


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

    with db_con:
        cursor = db_con.cursor()
        cursor.execute(sql)


def _get_connection(file: Path | None = None) -> sqlite3.Connection:
    """
    This function gets the database connection
    """
    if file is None:
        file = app_folder().joinpath("data.sqlite")

    init = False
    if not file.exists():
        init = True

    db_con = sqlite3.connect(file)
    db_con.row_factory = sqlite3.Row

    if init:
        _init_database(db_con)

    return db_con


def insert_location(record: Location, file: Path | None = None) -> bool:
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
                                 record.region, record.country_code, record.country, record.post_codes))
    except sqlite3.IntegrityError as e:
        if str(e) == 'UNIQUE constraint failed: project.name':
            raise DuplicateRecordError(f"A location with the name: {record.name} already exists.")
        raise
    else:
        return cursor.lastrowid > 0
    finally:
        con.close()


def update_location(record: Location, file: Path | None = None) -> bool:
    """
    This function updates a database record
    """
    sql = """UPDATE location SET location = ?, latitude = ?, longitude = ?, timezone = ?, region = ?, 
                    country_code = ?, country = ?, post_codes =?, lock_version = lock_version + 1, 
                    updated_at = CURRENT_TIMESTAMP WHERE (name = ?);"""

    con = _get_connection(file)

    try:
        with con:
            cursor = con.cursor()
            cursor.execute(sql, (record.location, record.latitude, record.longitude, record.timezone,
                                 record.region, record.country_code, record.country, record.post_codes, record.name))
        return cursor.rowcount == 1
    finally:
        con.close()


def delete_location(name: str, file: Path | None = None) -> bool:
    """
    This function deletes a database record
    """
    sql = """DELETE FROM location WHERE (name = ?);"""

    con = _get_connection(file)

    try:
        cursor = con.cursor()
        cursor.execute(sql, (name,))
        return cursor.rowcount == 1
    finally:
        con.close()


def get_location(name: str, file: Path | None = None) -> LocationRecord:
    """
    Gets the location record for a given name
    """
    sql = """SELECT name, location, latitude, longitude, timezone, region, country_code, country, post_codes, 
                lock_version, created_at, updated_at FROM location"""

    con = _get_connection(file)

    try:
        cursor = con.cursor()
        cursor.execute(sql)
        row = cursor.fetchone()
        if row:
            return LocationRecord(*row)
    finally:
        con.close()


def all_locations(file: Path | None = None) -> Locations | None:
    """
    This function returns all the location records in the database
    """
    sql = """SELECT name, latitude, longitude, country_code, country, post_codes, 
                lock_version, created_at, updated_at FROM location"""

    con = _get_connection(file)

    try:
        cursor = con.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        if rows:
            records = list()
            for row in rows:
                records.append(LocationRecordMetadata(*row))
            return Locations(records)
    finally:
        con.close()
