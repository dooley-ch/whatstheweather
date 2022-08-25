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

__all__ = ['Location', 'Forecast']

import attrs
import pendulum

@attrs.frozen
class Location:
    name: str = attrs.field(validator=attrs.validators.instance_of(str))
    latitude: float = attrs.field(validator=attrs.validators.instance_of(float))
    longitude: float = attrs.field(validator=attrs.validators.instance_of(float))
    region: str = attrs.field(validator=attrs.validators.instance_of(str))
    country_code: str = attrs.field(validator=attrs.validators.instance_of(str))
    country: str = attrs.field(validator=attrs.validators.instance_of(str))
    timezone: str = attrs.field(validator=attrs.validators.instance_of(str))
    post_codes: list[str] = attrs.Factory(list)


@attrs.frozen
class Forecast:
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
