# *******************************************************************************************
#  File:  model.py
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

__all__ = ['Location', 'LocationRecord', 'LocationRecordMetadata', 'Locations', 'Forecast']

from collections import UserList
from typing import Any
import attrs
import pendulum


def _convert_post_codes(post_codes: Any) -> Any:
    """
    Converts a list of postal codes to a string
    """
    if isinstance(post_codes, list):
        return "".join(post_codes)

    return post_codes


@attrs.frozen
class Location:
    """
    This class represents the geographical details of a location
    """
    name: str = attrs.field(validator=attrs.validators.instance_of(str))
    location: str = attrs.field(validator=attrs.validators.instance_of(str))
    latitude: float = attrs.field(validator=attrs.validators.instance_of(float), converter=float)
    longitude: float = attrs.field(validator=attrs.validators.instance_of(float), converter=float)
    region: str = attrs.field(validator=attrs.validators.instance_of(str))
    country_code: str = attrs.field(validator=attrs.validators.instance_of(str))
    country: str = attrs.field(validator=attrs.validators.instance_of(str))
    timezone: str = attrs.field(validator=attrs.validators.instance_of(str))
    post_codes: list[str] = attrs.field(factory=list, converter=_convert_post_codes)


@attrs.frozen
class LocationRecord(Location):
    """
    This class represents a database record for a location
    """
    lock_version: int = attrs.field(default=1, validator=attrs.validators.instance_of(int))
    created_at: pendulum.DateTime = attrs.field(factory=pendulum.now, converter=pendulum.parse,
                                                validator=attrs.validators.instance_of(pendulum.DateTime))
    updated_at: pendulum.DateTime = attrs.field(factory=pendulum.now, converter=pendulum.parse,
                                                validator=attrs.validators.instance_of(pendulum.DateTime))


@attrs.frozen
class LocationRecordMetadata:
    """
    This class provides the metadata about a location used to display a list of locations
    """
    name: str = attrs.field(validator=attrs.validators.instance_of(str))
    latitude: float = attrs.field(validator=attrs.validators.instance_of(float), converter=float)
    longitude: float = attrs.field(validator=attrs.validators.instance_of(float), converter=float)
    country_code: str = attrs.field(default='', validator=attrs.validators.instance_of(str))
    country: str = attrs.field(default='', validator=attrs.validators.instance_of(str))
    post_codes: str = attrs.field(default='', validator=attrs.validators.instance_of(str))
    lock_version: int = attrs.field(default=1, validator=attrs.validators.instance_of(int))
    created_at: pendulum.DateTime = attrs.field(factory=pendulum.now, converter=pendulum.parse,
                                                validator=attrs.validators.instance_of(pendulum.DateTime))
    updated_at: pendulum.DateTime = attrs.field(factory=pendulum.now, converter=pendulum.parse,
                                                validator=attrs.validators.instance_of(pendulum.DateTime))


class Locations(UserList):
    pass


@attrs.frozen
class Forecast:
    """
    This class represents a weather forecast for a given location
    """
    day: pendulum.Date = attrs.field(validator=attrs.validators.instance_of(pendulum.Date))
    weather_code: int = attrs.field(validator=attrs.validators.instance_of(int))
    weather_summary: str = attrs.field(validator=attrs.validators.instance_of(str))
    temp_max: float = attrs.field(validator=attrs.validators.instance_of(float))
    temp_min: float = attrs.field(validator=attrs.validators.instance_of(float))
    sunrise: pendulum.DateTime = attrs.field(validator=attrs.validators.instance_of(pendulum.DateTime))
    sunset: pendulum.DateTime = attrs.field(validator=attrs.validators.instance_of(pendulum.DateTime))
    precipitation_sum: float = attrs.field(validator=attrs.validators.instance_of(float))
    rain: float = attrs.field(validator=attrs.validators.instance_of(float))
    showers: float = attrs.field(validator=attrs.validators.instance_of(float))
    snowfall: float = attrs.field(validator=attrs.validators.instance_of(float))
    precipitation_hours: float = attrs.field(validator=attrs.validators.instance_of(float))
