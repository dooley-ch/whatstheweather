# *******************************************************************************************
#  File:  open_weather_map.py
#
#  Created: 04-07-2022
#
#  History:
#  04-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['get_location', 'get_weather']

from typing import TypedDict
import requests
from .app_types import UnitOfMeasure, Location, Locations, WeatherData, CurrentWeather, DailyWeather


class _GeoQueryParams(TypedDict):
    """
    Represents the parameters needed for a geo query
    """
    q: str
    limit: int
    appid: str


class _WeatherQueryParams(TypedDict):
    """
    Represents the parameters needed for a weather query
    """
    lon: float
    lat: float
    units: str
    exclude: str
    appid: str


# noinspection HttpUrlsUsage
def get_location(city: str, country_code: str, key: str, state: str | None = None, limit: int = 5) -> Locations | None:
    """
    This function returns the geolocation of a city
    """
    params: _GeoQueryParams = dict()
    if state:
        params['q'] = f"{city},{state},{country_code}"
    else:
        params['q'] = f"{city},{country_code}"
    params['limit'] = limit
    params['appid'] = key

    response = requests.get(url='http://api.openweathermap.org/geo/1.0/direct', params=params)
    if response.status_code == 200:
        data = response.json()

        results: Locations = Locations(list())
        for item in data:
            state = ''
            if 'state' in item:
                state = item['state']

            results.append(Location(item['name'], state, item['country'], item['lon'], item['lat']))

        return results


# noinspection HttpUrlsUsage
def get_weather(location: Location, state: str, country: str, key: str, unit_of_measure: UnitOfMeasure = UnitOfMeasure.Standard) -> WeatherData | None:
    """
    Gets the weather data for a given location
    """
    params: _WeatherQueryParams = dict()
    params['lon'] = location.longitude
    params['lat'] = location.latitude
    params['units'] = unit_of_measure.value
    params['exclude'] = 'hourly,minutely'
    params['appid'] = key

    response = requests.get(url='http://api.openweathermap.org/data/2.5/onecall', params=params)
    if response.status_code == 200:
        data = response.json()

        lat = data['lat']
        lon = data['lon']
        timezone = data['timezone']
        current_data = data['current']
        daily_data = data['daily']

        current = CurrentWeather.parse(current_data)

        weather = WeatherData(location.city, state, country, lat, lon, timezone, unit_of_measure, current)

        for item in daily_data:
            weather.daily_weather.append(DailyWeather.parse(item))

        return weather
