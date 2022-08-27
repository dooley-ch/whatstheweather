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

__all__ = ['Location', 'LocationRecord', 'LocationRecordMetadata', 'Locations', 'Forecast', 'Forecasts', 'CurrentWeather']

from collections import UserList
from typing import Any
import attrs
import pendulum
from rich.padding import Padding
from rich.table import Table


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
    post_codes: str = attrs.field(validator=attrs.validators.instance_of(str), converter=_convert_post_codes)

    def __rich__(self) -> Padding:
        table = Table(title=f"location: {self.name}", show_header=False, show_footer=False, style="table-style",
                      title_style="table-title-style", border_style="table-border-style")

        table.add_column("Attribute", justify='right')
        table.add_column("Value")

        table.add_row("Name:", self.name)
        table.add_row("Location:", self.location)
        table.add_row("Latitude:", str(self.latitude))
        table.add_row("Longitude:", str(self.longitude))
        table.add_row("Region:", self.region)
        table.add_row("Country Code:", self.country_code)
        table.add_row("Country:", self.country)
        table.add_row("Timezone", self.timezone)
        table.add_row("Post Codes:", self.post_codes)

        return Padding(table, (0, 0, 0, 3))


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
    region: str = attrs.field(default='', validator=attrs.validators.instance_of(str))
    country_code: str = attrs.field(default='', validator=attrs.validators.instance_of(str))
    country: str = attrs.field(default='', validator=attrs.validators.instance_of(str))
    post_codes: str = attrs.field(default='', validator=attrs.validators.instance_of(str))
    lock_version: int = attrs.field(default=1, validator=attrs.validators.instance_of(int))
    created_at: pendulum.DateTime = attrs.field(factory=pendulum.now, converter=pendulum.parse,
                                                validator=attrs.validators.instance_of(pendulum.DateTime))
    updated_at: pendulum.DateTime = attrs.field(factory=pendulum.now, converter=pendulum.parse,
                                                validator=attrs.validators.instance_of(pendulum.DateTime))


class Locations(UserList):
    """
    This collection houses the metadata for the locations store din the database
    """
    def __rich__(self) -> Padding:
        table = Table(title="locations", style="table-style", header_style="table-header-style",
                      title_style="table-title-style", row_styles=["table-odd-row-style", "table-even-row-style"],
                      border_style="table-border-style")

        table.add_column("Id", justify='right')
        table.add_column("Name")
        table.add_column("Latitude", justify='right')
        table.add_column("Longitude", justify='right')
        table.add_column("Region")
        table.add_column("Country")
        count = 0

        for item in self:
            count += 1
            table.add_row(str(count), item.name, str(item.latitude), str(item.longitude), item.region, item.country)

        return Padding(table, (0, 0, 0, 3))


@attrs.frozen
class CurrentWeather:
    """
    This class represents the current weather
    """
    temperature: float = attrs.field(validator=attrs.validators.instance_of(float))
    windspeed: float = attrs.field(validator=attrs.validators.instance_of(float))
    winddirection: float = attrs.field(validator=attrs.validators.instance_of(float))
    weather_code: int = attrs.field(validator=attrs.validators.instance_of(int))
    weather_summary: str = attrs.field(validator=attrs.validators.instance_of(str))
    current_time: pendulum.DateTime = attrs.field(validator=attrs.validators.instance_of(pendulum.DateTime))
    location: str = attrs.field(validator=attrs.validators.instance_of(str))

    def __rich__(self) -> Padding:
        """
        This method renders the class instance to the terminal
        """
        table = Table(title=f"Current Weather: {self.location} ({self.current_time.to_iso8601_string()})",
                      style="table-style", show_header=False, show_footer=False,
                      border_style="table-border-style", title_style="table-title-style",
                      row_styles=["table-odd-row-style", "table-even-row-style"])

        table.add_column("Parameter", justify='right')
        table.add_column("Value")

        table.add_row("Summary", self.weather_summary)
        table.add_row("Temperature", str(self.temperature))
        table.add_row("Wind Speed", str(self.windspeed))
        table.add_row("Wind Direction", str(self.winddirection))

        return Padding(table, (0, 0, 0, 3))


@attrs.frozen
class Forecast:
    """
    This class represents a weather forecast for a given location
    """
    location: str = attrs.field(validator=attrs.validators.instance_of(str))
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

    def __rich__(self) -> Padding:
        """
        This method renders the class instance to the terminal
        """
        table = Table(title=f"Forecast for: {self.location}", style="table-style", show_header=False, show_footer=False,
                      border_style="table-border-style", title_style="table-title-style",
                      row_styles=["table-odd-row-style", "table-even-row-style"])

        table.add_column("Parameter", justify='right')
        table.add_column("Value")

        table.add_row("Date", self.day.to_date_string())
        table.add_row("Summary", self.weather_summary)
        table.add_row("Max Temperature", str(self.temp_max))
        table.add_row("Min Temperature", str(self.temp_min))
        table.add_row("Sunrise", self.sunrise.to_iso8601_string())
        table.add_row("Sunset", self.sunset.to_iso8601_string())
        table.add_row("Total Precipitation", str(self.precipitation_sum))
        table.add_row("Precipitation Hours", str(self.precipitation_hours))
        table.add_row("Rain", str(self.rain))
        table.add_row("Showers", str(self.showers))
        table.add_row("Snowfall", str(self.snowfall))

        return Padding(table, (0, 0, 0, 3))


class Forecasts(UserList):
    """
    This collection houses the metadata for the locations store din the database
    """
    def __rich__(self) -> Padding:
        forecast = self[0]

        table = Table(title=f"Forecast for: {forecast.location}", style="table-style", header_style="table-header-style",
                      title_style="table-title-style", row_styles=["table-odd-row-style", "table-even-row-style"],
                      border_style="table-border-style")

        table.add_column("Date")
        table.add_column("Summary")
        table.add_column("Max Temperature", justify="right")
        table.add_column("Min Temperature", justify="right")
        table.add_column("Sunrise")
        table.add_column("Sunset")
        table.add_column("Total Precipitation", justify="right")
        table.add_column("Precipitation Hours", justify="right")
        table.add_column("Rain", justify="right")
        table.add_column("Showers", justify="right")
        table.add_column("Snowfall", justify="right")

        for item in self:
            table.add_row(item.day.to_date_string(), item.weather_summary, str(item.temp_max), str(item.temp_min),
                          item.sunrise.to_iso8601_string(), item.sunset.to_iso8601_string(), str(item.precipitation_sum),
                          str(item.precipitation_hours), str(item.rain), str(item.showers), str(item.snowfall))

        return Padding(table, (0, 0, 0, 3))
