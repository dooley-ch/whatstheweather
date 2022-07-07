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

__all__ = ['init_database']


import csv
from pprint import pprint
from typing import NewType
from pathlib import Path
import attrs


# region Validators

def is_2_char_validator(instance, attribute, value):
    """
    This function ensures the field value is exactly two chars long
    """
    if len(value) != 2:
        raise ValueError(f"value ({value}) must be exactly 2 characters long")


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


ImportStates = NewType('ImportCountries', list[_ImportedState])


@attrs.frozen
class _ImportCountry:
    """
    Represents a country in the import file
    """
    iso_2: str = attrs.field(validator=[attrs.validators.instance_of(str), is_2_char_validator])
    iso_3: str = attrs.field(validator=[attrs.validators.instance_of(str), is_3_char_validator])
    name: str = attrs.field(validator=[attrs.validators.instance_of(str)])

ImportCountries = NewType('ImportCountries', list[_ImportCountry])


def _load_states(file: Path) -> ImportStates:
    contents = ImportStates(list())
    rows = csv.DictReader(file.open('r'))
    for row in rows:
        contents.append(_ImportedState(**row))

    return contents


def _load_countries(file: Path) -> ImportCountries:
    contents = ImportCountries(list())
    rows = csv.DictReader(file.open('r'))
    for row in rows:
        contents.append(_ImportCountry(**row))

    return contents


def init_database(app_folder: Path, data_folder: Path) -> bool | None:
    """
    This function creates and populates the application database
    """
    countries_file = data_folder.joinpath('countries.csv')
    if not countries_file.exists():
        raise FileNotFoundError(f'File not found: {countries_file}')

    states_file = data_folder.joinpath('states.csv')
    if not states_file.exists():
        f'File not found: {states_file}'

    countries = _load_countries(countries_file)
    states = _load_states(states_file)

    for item in countries:
        pprint(item)

    for item in states:
        pprint(item)
