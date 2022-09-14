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

__all__ = ['Location', 'Forecast', 'CurrentWeather', 'Locations', 'Forecasts']

import enum
import related
from rich.padding import Padding
from rich.table import Table


@enum.unique
class Result(enum.Enum):
    """
    This enum represents the outcome of an operation
    """
    Success = 1
    Fail = 2
    NoOperation = 3


@related.immutable
class Location:
    """
    This class represents the geographical details of a location
    """
    name = related.StringField(required=True)
    location = related.StringField(required=True)
    longitude = related.FloatField(required=True)
    latitude = related.FloatField(required=True)
    region = related.StringField(required=True)
    country_code = related.StringField(required=True)
    country = related.StringField(required=True)
    timezone = related.StringField(required=True)
    post_codes = related.SequenceField(str, default=list())
    lock_version = related.IntegerField(required=False)
    created_at = related.DateTimeField(required=False)
    updated_at = related.DateTimeField(required=False)

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
        table.add_row("Post Codes:", ''.join(self.post_codes))

        return Padding(table, (0, 0, 0, 3))


class Locations(list):
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

        for row_number, item in enumerate(self):
            table.add_row(str(row_number), item.name, str(item.latitude), str(item.longitude), item.region, item.country)

        return Padding(table, (0, 0, 0, 3))


@related.immutable
class CurrentWeather:
    """
    This class represents the current weather
    """
    temperature = related.FloatField(required=True)
    windspeed = related.FloatField(required=True)
    winddirection = related.FloatField(required=True)
    weather_code = related.IntegerField(required=True)
    weather_summary = related.StringField(required=True)
    current_time = related.DateTimeField(required=True)
    location = related.StringField(required=True)

    # def __rich__(self) -> Padding:
    #     """
    #     This method renders the class instance to the terminal
    #     """
    #     table = Table(title=f"Current Weather: {self.location} ({self.current_time.to_iso8601_string()})",
    #                   style="table-style", show_header=False, show_footer=False,
    #                   border_style="table-border-style", title_style="table-title-style",
    #                   row_styles=["table-odd-row-style", "table-even-row-style"])
    #
    #     table.add_column("Parameter", justify='right')
    #     table.add_column("Value")
    #
    #     table.add_row("Summary", self.weather_summary)
    #     table.add_row("Temperature", f"{self.temperature}°C")
    #     table.add_row("Wind Speed", f"{self.windspeed} km/h")
    #     table.add_row("Wind Direction", _convert_degrees_direction(self.winddirection))
    #
    #     return Padding(table, (0, 0, 0, 3))


@related.immutable()
class Forecast:
    """
    This class represents a weather forecast for a given location
    """
    location = related.StringField(required=True)
    day = related.DateField(required=True)
    weather_code = related.IntegerField(required=True)
    weather_summary = related.StringField(required=True)
    temp_max = related.FloatField(required=True)
    temp_min = related.FloatField(required=True)
    sunrise = related.DateTimeField(required=True)
    sunset = related.DateTimeField(required=True)
    precipitation_sum = related.FloatField(required=True)
    rain = related.FloatField(required=True)
    showers = related.FloatField(required=True)
    snowfall = related.FloatField(required=True)
    precipitation_hours = related.FloatField(required=True)
    wind_speed = related.FloatField(required=True)
    wind_direction = related.FloatField(required=True)

    # def __rich__(self) -> Padding:
    #     """
    #     This method renders the class instance to the terminal
    #     """
    #     table = Table(title=f"Forecast for: {self.location}", style="table-style", show_header=False,
    #     show_footer=False,
    #                   border_style="table-border-style", title_style="table-title-style",
    #                   row_styles=["table-odd-row-style", "table-even-row-style"])
    #
    #     table.add_column("Parameter", justify='right')
    #     table.add_column("Value")
    #
    #     table.add_row("Date", self.day.to_date_string())
    #     table.add_row("Summary", self.weather_summary)
    #     table.add_row("Max Temperature", f"{self.temp_max}°C")
    #     table.add_row("Min Temperature", f"{self.temp_min}°C")
    #     table.add_row("Sunrise", self.sunrise.to_iso8601_string())
    #     table.add_row("Sunset", self.sunset.to_iso8601_string())
    #     table.add_row("Total Precipitation", f"{self.precipitation_sum}mm")
    #     table.add_row("Precipitation Hours", f"{self.precipitation_hours} hours")
    #     table.add_row("Rain", f"{self.rain}mm")
    #     table.add_row("Showers", f"{self.showers}mm")
    #     table.add_row("Snowfall", f"{self.snowfall}cm")
    #     table.add_row("Wind Speed", f"{self.wind_speed} km/h")
    #     table.add_row("Wind Direction", _convert_degrees_direction(self.wind_direction))
    #
    #     return Padding(table, (0, 0, 0, 3))


class Forecasts(list):
    pass

# class Forecasts(UserList):
#     """
#     This collection houses the metadata for the locations store din the database
#     """
#     def __rich__(self) -> Padding:
#         forecast = self[0]
#
#         table = Table(title=f"Forecast for: {forecast.location}", style="table-style",
#         header_style="table-header-style",
#                       title_style="table-title-style", row_styles=["table-odd-row-style", "table-even-row-style"],
#                       border_style="table-border-style")
#
#         table.add_column("Date")
#         table.add_column("Summary")
#         table.add_column("Max Temp.", justify="right")
#         table.add_column("Min Temp.", justify="right")
#         table.add_column("Sunrise")
#         table.add_column("Sunset")
#         table.add_column("Precipitation", justify="right")
#         table.add_column("Precipitation Hours", justify="right")
#         table.add_column("Rain", justify="right")
#         table.add_column("Showers", justify="right")
#         table.add_column("Snowfall", justify="right")
#         table.add_column("Wind Speed", justify="right")
#         table.add_column("Wind Direction", justify="center")
#
#         for item in self:
#             table.add_row(item.day.to_date_string(), item.weather_summary, f"{item.temp_max}°C", f"{item.temp_min}°C",
#                           item.sunrise.to_iso8601_string(), item.sunset.to_iso8601_string(),
#                           f"{item.precipitation_sum}mm",
#                           f"{item.precipitation_hours} hours", f"{item.rain}mm", f"{item.showers}mm",
#                           f"{item.snowfall}cm",
#                           f"{item.wind_speed} km/h", _convert_degrees_direction(item.wind_direction))
#
#         return Padding(table, (0, 0, 0, 3))
