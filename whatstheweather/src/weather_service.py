# *******************************************************************************************
#  File:  weather_service.py
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

__all__ = ['get_locations', 'get_forecast', 'get_current_weather']

from time import sleep

import pendulum
import requests
from rich.console import Console
from loguru import logger
from . model import Location, Forecast, Locations, Forecasts, CurrentWeather


_console = Console()


def _get_summary(code: int) -> str:
    match code:
        case 0:
            return 'Clear sky'
        case 1 | 2 | 3:
            return 'Mainly clear, partly cloudy, and overcast'
        case 45 | 48:
            return 'Fog and depositing rime fog'
        case 51 | 53 | 55:
            return 'Drizzle: Light, moderate, and dense intensity'
        case 56 | 57:
            return 'Freezing Drizzle: Light and dense intensity'
        case 61 | 63 | 65:
            return 'Rain: Slight, moderate and heavy intensity'
        case 66 | 67:
            return 'Freezing Rain: Light and heavy intensity'
        case 71 | 73 | 75:
            return 'Snow fall: Slight, moderate, and heavy intensity'
        case 77:
            return 'Snow grains'
        case 80 | 81 | 82:
            return 'Rain showers: Slight, moderate, and violent'
        case 85 | 86:
            return 'Snow showers slight and heavy'
        case 95:
            return 'Thunderstorm: Slight or moderate'
        case 96 | 99:
            return 'Thunderstorm with slight and heavy hail'
        case _:
            return 'Unknown'


def get_current_weather(location: str, lat: float, long: float, timezone: str) -> CurrentWeather:
    """
    This function returns the weather forecast at the given location

    :param location: The location requested
    :param lat: The latitude for the location to report on
    :param long:  The longitude for the location to report on
    :param timezone: The time zone for the given location
    :return: The 7-day forecast for the given location
    """
    params = {
        "latitude": lat,
        "longitude": long,
        "daily": ['weathercode', 'temperature_2m_max', 'temperature_2m_min', 'sunrise', 'sunset', 'precipitation_sum',
                  'rain_sum', 'showers_sum', 'snowfall_sum', 'precipitation_hours'],
        "timezone": timezone,
        "current_weather": "true"
    }

    try:
        with _console.status("Downloading current weather..."):
            sleep(2)
            response = requests.get(url='https://api.open-meteo.com/v1/forecast', params=params)
    except Exception as e:
        logger.error(f"Failed to get forecast data: ({lat},{long}), {timezone} - {e}")
        raise

    if response.status_code == 200:
        data = response.json()['current_weather']

        time = pendulum.parse(data['time'])
        weather_code = int(data['weathercode'])
        weather_summary = _get_summary(weather_code)
        temperature = data['temperature']
        windspeed = data['windspeed']
        winddirection = data['winddirection']

        return CurrentWeather(temperature, windspeed, winddirection, weather_code, _get_summary(weather_code),
                              time, location)
    else:
        logger.error(
            f"Failed to obtain current weather data: ({lat},{long}), {timezone} - {response.status_code} - {response.text}")


def get_forecast(location: str, lat: float, long: float, timezone: str) -> Forecasts:
    """
    This function returns the weather forecast at the given location

    :param location: The location requested
    :param lat: The latitude for the location to report on
    :param long:  The longitude for the location to report on
    :param timezone: The time zone for the given location
    :return: The 7-day forecast for the given location
    """
    params = {
        "latitude": lat,
        "longitude": long,
        "daily": ['weathercode', 'temperature_2m_max', 'temperature_2m_min', 'sunrise', 'sunset', 'precipitation_sum',
                  'rain_sum', 'showers_sum', 'snowfall_sum', 'precipitation_hours', 'windspeed_10m_max',
                  'winddirection_10m_dominant'],
        "timezone": timezone
    }

    try:
        with _console.status("Downloading weather forecast..."):
            sleep(2)
            response = requests.get(url='https://api.open-meteo.com/v1/forecast', params=params)
    except Exception as e:
        logger.error(f"Failed to get forecast data: ({lat},{long}), {timezone} - {e}")
        raise

    if response.status_code == 200:
        data = response.json()['daily']

        forecasts = list()

        for i in range(0, len(data['time'])):
            day = pendulum.parse(data['time'][i])
            weather_code = int(data['weathercode'][i])
            weather_summary = _get_summary(weather_code)
            temp_max = data['temperature_2m_max'][i]
            temp_min = data['temperature_2m_min'][i]
            sunrise = pendulum.parse(data['sunrise'][i])
            sunset = pendulum.parse(data['sunset'][i])
            precipitation_sum = data['precipitation_sum'][i]
            rain = data['rain_sum'][i]
            showers = data['showers_sum'][i]
            snowfall = data['snowfall_sum'][i]
            precipitation_hours = data['precipitation_hours'][i]
            windspeed = data['windspeed_10m_max'][i]
            winddirection = data['winddirection_10m_dominant'][i]

            forecasts.append(Forecast(location, day, weather_code, weather_summary, temp_max, temp_min, sunrise, sunset,
                                      precipitation_sum, rain, showers, snowfall, precipitation_hours, windspeed,
                                      winddirection))

        return Forecasts(forecasts)
    else:
        logger.error(
            f"Failed to obtain forecast data: ({lat},{long}), {timezone} - {response.status_code} - {response.text}")


def get_locations(name: str, limit: int = 10) -> Locations | None:
    """
    This function returns the lookup entries for a given location name

    :param name: The name of the location
    :param limit: The number of entries to return
    :return: The lost of possible locations matching the name given
    """
    params = {"name": name, "count": limit}

    try:
        with _console.status("Downloading locations..."):
            sleep(2)
            response = requests.get(url='https://geocoding-api.open-meteo.com/v1/search', params=params)
    except Exception as e:
        logger.error(f"Failed to get location: {name} - {e}")
        raise

    if response.status_code == 200:
        response_data = response.json()
        if 'results' not in response_data:
            return None
        data = response_data['results']
        locations = list()

        for item in data:
            name = item['name']
            latitude = item['latitude']
            longitude = item['longitude']
            region = item['admin1'] if 'admin1' in item else ''
            country_code = item['country_code']
            country = item['country'] if 'country' in item else ''
            timezone = item['timezone']
            post_codes = item['postcodes'] if 'postcodes' in item else []

            locations.append(
                Location(name, name, latitude, longitude, region, country_code, country, timezone, post_codes))

        return Locations(locations)
    else:
        logger.error(f"Failed to obtain location data: {name} - {response.status_code} - {response.text}")
