# *******************************************************************************************
#  File:  database_test.py
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

__all__ = []

from whatstheweather.src.model import Location
from whatstheweather.src.data import insert_location, update_location, delete_location, get_location, all_locations


def test_insert_location(db_file_name) -> None:
    location = Location("Langenthal", "Langenthal", 47.21526, 7.79607, "Europe/Zurich", "Bern", "CH", "Switzerland", ["4900"])
    assert insert_location(location, db_file_name)


def test_update_location(db_file_name) -> None:
    location = Location("Langenthal", "Langenthal", 47.21526, 7.79607, "Europe/Zurich", "Bern", "CH", "Switzerland", ["4900"])
    assert insert_location(location, db_file_name)

    location = Location("Langenthal", "Langenthal", 47.21526, 7.79607, "Europe/Zurich", "Bern", "CH", "Switzerland", ["4905"])
    assert update_location(location, db_file_name)


def test_delete_location(db_file_name) -> None:
    location = Location("Langenthal", "Langenthal", 47.21526, 7.79607, "Europe/Zurich", "Bern", "CH", "Switzerland", ["4900"])
    assert insert_location(location, db_file_name)

    assert delete_location("Langenthal", db_file_name)


def test_get_location(db_file_name) -> None:
    location = Location("Langenthal", "Langenthal", 47.21526, 7.79607, "Europe/Zurich", "Bern", "CH", "Switzerland", ["4900"])
    assert insert_location(location, db_file_name)

    record = get_location("Langenthal")
    assert record


def test_all_locations(db_file_name) -> None:
    location = Location("Langenthal-01", "Langenthal", 47.21526, 7.79607, "Europe/Zurich", "Bern", "CH", "Switzerland", ["4900"])
    assert insert_location(location, db_file_name)
    location = Location("Langenthal-02", "Langenthal", 47.21526, 7.79607, "Europe/Zurich", "Bern", "CH", "Switzerland", ["4900"])
    assert insert_location(location, db_file_name)
    location = Location("Langenthal-03", "Langenthal", 47.21526, 7.79607, "Europe/Zurich", "Bern", "CH", "Switzerland", ["4900"])
    assert insert_location(location, db_file_name)
    location = Location("Langenthal-04", "Langenthal", 47.21526, 7.79607, "Europe/Zurich", "Bern", "CH", "Switzerland", ["4900"])
    assert insert_location(location, db_file_name)

    records = all_locations(db_file_name)
    assert len(records) == 4
