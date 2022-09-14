# *******************************************************************************************
#  File:  _weather.py
#
#  Created: 14-09-2022
#
#  History:
#  14-09-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['current', 'forecast']

from .. import ui
from .. import data
from .. import weather_service
from .. import model


def current(location: str) -> None:
    """
    This function gets the current weather at the given location
    """
    location = location.title()

    record = data.get_location_record(location)
    if record is None:
        ui.console.line(1)
        ui.system_message(f"Location ({location}) not found, add it before requesting current weather.")
        ui.console.line(1)
        return

    weather = weather_service.get_current_weather(record.location, record.latitude, record.longitude, record.timezone)
    if weather is None:
        ui.console.line(1)
        ui.system_message(f"Unable to obtain current weather for location ({location}).")
        ui.console.line(1)
        return

    screen = model.CurrentWeatherScreen(record, weather)
    ui.console.clear()
    ui.console.line(1)
    ui.console.print(screen)


def forecast(location: str) -> None:
    """
    This function gets the weather forecast for a given location
    """
    location = location.title()

    record = data.get_location_record(location)
    if record is None:
        ui.console.line(1)
        ui.system_message(f"Location ({location}) not found, add it before requesting weather forecast")
        ui.console.line(1)
        return

    forecasts = weather_service.get_forecast(record.location, record.latitude, record.longitude, record.timezone)
    if forecasts is None:
        ui.console.line(1)
        ui.system_message(f"Unable to obtain weather forecast for location ({location}).")
        ui.console.line(1)
        return

    screen = model.WeatherForecastScreen(record, forecasts)
    ui.console.clear()
    ui.console.line(1)
    ui.console.print(screen)
