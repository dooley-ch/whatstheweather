# *******************************************************************************************
#  File:  data.py
#
#  Created: 07-07-2022
#
#  History:
#  07-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['init_database', 'get_state_by_code', 'get_state_by_name', 'is_valid_state', 'is_valid_state_code',
           'get_country_by_name', 'get_country_by_iso_3', 'get_country_by_iso_2', 'is_valid_country_name',
           'is_valid_iso_3_country_code', 'is_valid_iso_2_country_code']

import csv
from pathlib import Path
from enum import Enum
import attrs
import tinydb
from .app_types import Country, State


def _get_database_file(app_folder: Path) -> Path:
    """
    Returns the database file name
    """
    return app_folder.joinpath('data.json')


class _DocumentType(str, Enum):
    """
    This enum defines the type of document stored in the database
    """
    State = 'state'
    Country = 'country'


# region Validators

# noinspection DuplicatedCode,PyUnusedLocal
def is_2_char_validator(instance, attribute, value):
    """
    This function ensures the field value is exactly two chars long
    """
    if len(value) != 2:
        raise ValueError(f"value ({value}) must be exactly 2 characters long")


# noinspection PyUnusedLocal
def is_3_char_validator(instance, attribute, value):
    """
    This function ensures the field value is exactly two chars long
    """
    if len(value) != 3:
        raise ValueError(f"value ({value}) must be exactly 3 characters long")


# endregion

@attrs.frozen
class _ImportedState:
    """
    Represents a state entry in the import file
    """
    state: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    abb: str = attrs.field(validator=[attrs.validators.instance_of(str), is_2_char_validator])
    capital: str = attrs.field(validator=[attrs.validators.instance_of(str)])
    region: str = attrs.field(validator=[attrs.validators.instance_of(str)])


@attrs.frozen
class _StatesDocument:
    """
    This class defines the states document stored in the database
    """
    document_type: _DocumentType = attrs.field(default=_DocumentType.State)
    states: list[_ImportedState] = attrs.Factory(list)


@attrs.frozen
class _ImportCountry:
    """
    Represents a country in the import file
    """
    iso_2: str = attrs.field(validator=[attrs.validators.instance_of(str), is_2_char_validator])
    iso_3: str = attrs.field(validator=[attrs.validators.instance_of(str), is_3_char_validator])
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])


@attrs.frozen
class _CountryDocument:
    """
    This class defines the country document stored in the database
    """
    document_type: _DocumentType = attrs.field(default=_DocumentType.Country)
    countries: list[_ImportCountry] = attrs.Factory(list)


def _load_states(file: Path) -> _StatesDocument:
    """
    This function loads the states' data from the csv file and
    returns it as a document ready to store in the application database
    """
    contents = _StatesDocument()
    rows = csv.DictReader(file.open('r'))
    for row in rows:
        contents.states.append(_ImportedState(**row))

    return contents


def _load_countries(file: Path) -> _CountryDocument:
    """
    This function loads the countries' data from the csv file and
    returns it as a document ready to store in the application database
    """
    contents = _CountryDocument()
    rows = csv.DictReader(file.open('r'))
    for row in rows:
        contents.countries.append(_ImportCountry(**row))

    return contents


def _get_countries(app_folder: Path) -> list[Country]:
    db = tinydb.TinyDB(_get_database_file(app_folder))
    data = db.search(tinydb.where("document_type") == "country")
    country_data = data[0]['countries']

    results = list()

    for item in country_data:
        iso_2 = item['iso_2']
        iso_3 = item['iso_3']
        name = item['name']
        results.append(Country(iso_2, iso_3,  name))

    return results


def _get_states(app_folder: Path) -> list[State]:
    db = tinydb.TinyDB(_get_database_file(app_folder))
    data = db.search(tinydb.where("document_type") == "state")
    state_data = data[0]['states']

    results = list()

    for item in state_data:
        state = item['state']
        abb = item['abb']
        capital = item['capital']
        region = item['region']
        results.append(State(abb, state, capital, region))

    return results


def init_database(app_folder: Path, data_folder: Path) -> None:
    """
    This function creates and populates the application database
    """
    # noinspection DuplicatedCode
    countries_file = data_folder.joinpath('countries.csv')
    if not countries_file.exists():
        raise FileNotFoundError(f'File not found: {countries_file}')

    states_file = data_folder.joinpath('states.csv')
    if not states_file.exists():
        f'File not found: {states_file}'

    country_doc = _load_countries(countries_file)
    state_doc = _load_states(states_file)

    database_file = _get_database_file(app_folder)
    if database_file.exists():
        database_file.unlink()

    db = tinydb.TinyDB(database_file)

    db.insert(attrs.asdict(country_doc))
    db.insert(attrs.asdict(state_doc))


def is_valid_state_code(app_folder: Path, code: str) -> bool:
    """
     This function returns true if the name is valid
     """
    states = _get_states(app_folder)

    for state in states:
        if state.code == code:
            return True

    return False


def is_valid_state(app_folder: Path, name: str) -> bool:
    """
     This function returns true if the name is valid
     """
    states = _get_states(app_folder)

    for state in states:
        if state.name == name:
            return True

    return False


def get_state_by_code(app_folder: Path, code: str) -> State | None:
    """
     This function returns the state record if the code is valid
     """
    states = _get_states(app_folder)

    for state in states:
        if state.code == code:
            return state


def get_state_by_name(app_folder: Path, name: str) -> State | None:
    """
     This function returns the state record if the name is valid
     """
    states = _get_states(app_folder)

    for state in states:
        if state.name == name:
            return state


def is_valid_country_name(app_folder: Path, nane: str) -> bool:
    """
    This function returns a true if the country code is valid, otherwise false
    """
    countries = _get_countries(app_folder)

    for country in countries:
        if country.name == nane:
            return True

    return False


def is_valid_iso_3_country_code(app_folder: Path, code: str) -> bool:
    """
    This function returns a true if the country code is valid, otherwise false
    """
    countries = _get_countries(app_folder)

    for country in countries:
        if country.iso_3 == code:
            return True

    return False


def is_valid_iso_2_country_code(app_folder: Path, code: str) -> bool:
    """
    This function returns a true if the country code is valid, otherwise false
    """
    countries = _get_countries(app_folder)

    for country in countries:
        if country.iso_2 == code:
            return True

    return False


def get_country_by_name(app_folder: Path, name: str) -> Country | None:
    """
    This function returns a country record based on the country name
    """
    countries = _get_countries(app_folder)

    for country in countries:
        if country.name == name:
            return country


def get_country_by_iso_3(app_folder: Path, code: str) -> Country | None:
    """
    This function returns a country record based on the country's iso 3 code
    """
    countries = _get_countries(app_folder)

    for country in countries:
        if country.iso_3 == code:
            return country


def get_country_by_iso_2(app_folder: Path, code: str) -> Country | None:
    """
    This function returns a country record based on the country's iso 2 code
    """
    countries = _get_countries(app_folder)

    for country in countries:
        if country.iso_2 == code:
            return country
