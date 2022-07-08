# *******************************************************************************************
#  File:  types.py
#
#  Created: 04-07-2022
#
#  History:
#  04-07-2022: Initial version
#
# *******************************************************************************************
from __future__ import annotations

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['UnitOfMeasure', 'Location', 'Locations', 'WeatherData', 'Weather', 'CurrentWeather', 'DailyWeather',
           'WeatherReportParams', 'Country', 'State']

import enum
import typing
import attrs
import pendulum


def _from_timestamp_to_date(value: int) -> pendulum.DateTime:
    """
    This function is used by attrs to convert timestamp values to DateTime instances
    by some DTO classes via a converter attribute on the field definition
    """
    return pendulum.from_timestamp(value)


class Country(typing.NamedTuple):
    """
    This class holds the name and iso code for a country
    """
    iso_2: str
    iso_3: str
    name: str


class State(typing.NamedTuple):
    """
    This class holds the name and iso code for a state
    """
    code: str
    name: str
    capital: str
    region: str


class UnitOfMeasure(str, enum.Enum):
    """
    This enum represents the reporting unit of measure
    """
    Standard = 'standard'
    Metric = 'metric'
    Imperial = 'imperial'


@attrs.frozen
class WeatherReportParams:
    """
    This class represents the parameters needed to generate a weather report
    """
    city: str
    state: str
    country: str
    longitude: float
    latitude: float
    unit_of_measure: UnitOfMeasure
    api_key: str


class Location(typing.NamedTuple):
    """
    This class holds the geographic location of a city
    """
    city: str
    state: str
    country: str
    longitude: float
    latitude: float

    def __repr__(self):
        return f"{self.city}, {self.state}, {self.country} ({self.latitude}, {self.longitude})"


Locations = typing.NewType('Locations', list[Location])


class Temperature(typing.TypedDict):
    """
    This class represents the data structure returned by the OpenWeatherMap site for temperature
    entries
    """
    day: float
    min: float
    max: float
    night: float
    eve: float
    morn: float


class FeelsLike(typing.TypedDict):
    """
    This class represents the data structure returned by the OpenWeatherMap site for 'feels like'
    entries
    """
    day: float
    night: float
    eve: float
    morn: float


@attrs.frozen
class Weather:
    """
    This class represents the data structure returned by the OpenWeatherMap site for weather
    entries
    """
    id: int
    main: str
    description: str
    icon: str


@attrs.frozen()
class CurrentWeather:
    """
    This class represents the data structure returned by the OpenWeatherMap site for current weather entry
    """
    dt: pendulum.DateTime = attrs.field(converter=_from_timestamp_to_date)
    sunrise: pendulum.DateTime = attrs.field(converter=_from_timestamp_to_date)
    sunset: pendulum.DateTime = attrs.field(converter=_from_timestamp_to_date)
    pressure: int
    humidity: int
    clouds: int
    visibility: int
    wind_speed: float
    wind_deg: float
    weather: list[Weather] = attrs.Factory(dict)
    temp: Temperature = attrs.Factory(dict)
    feels_like: FeelsLike = attrs.Factory(dict)

    @classmethod
    def parse(cls, data: dict[str, typing.Any]) -> CurrentWeather:
        dt = data['dt']
        sunrise = data['sunrise']
        sunset = data['sunset']
        pressure = data['pressure']
        humidity = data['humidity']
        clouds = data['clouds']
        visibility = data['visibility']
        wind_speed = data['wind_speed']
        wind_deg = data['wind_deg']
        weather = data['weather']
        temp = data['temp']
        feels_like = data['feels_like']

        return CurrentWeather(dt, sunrise, sunset, pressure, humidity, clouds, visibility,
                              wind_speed, wind_deg, weather, temp, feels_like)


@attrs.frozen
class DailyWeather:
    """
    This class represents the data structure returned by the OpenWeatherMap site for daily weather
    entries
    """
    dt: pendulum.DateTime = attrs.field(converter=_from_timestamp_to_date)
    sunrise: pendulum.DateTime = attrs.field(converter=_from_timestamp_to_date)
    sunset: pendulum.DateTime = attrs.field(converter=_from_timestamp_to_date)
    pressure: int
    humidity: int
    wind_speed: float
    wind_deg: float
    clouds: int
    weather: list[Weather] = attrs.Factory(dict)
    temp: Temperature = attrs.Factory(dict)
    feels_like: FeelsLike = attrs.Factory(dict)

    @classmethod
    def parse(cls, data: dict[str, typing.Any]) -> DailyWeather:
        dt = data['dt']
        sunrise = data['sunrise']
        sunset = data['sunset']
        pressure = data['pressure']
        humidity = data['humidity']
        wind_speed = data['wind_speed']
        wind_deg = data['wind_deg']
        clouds = data['clouds']
        weather = data['weather']
        temp = data['temp']
        feels_like = data['feels_like']

        return DailyWeather(dt, sunrise, sunset, pressure, humidity, wind_speed, wind_deg, clouds,
                            weather, temp, feels_like)


@attrs.frozen
class WeatherData:
    """
    This class holds all the weather data returned by the OpenWeatherMap data service for a given city.
    """
    city: str
    state: str
    country: str
    longitude: float
    latitude: float
    timezone: str
    current_weather: CurrentWeather
    daily_weather: list[DailyWeather] = attrs.Factory(list)
