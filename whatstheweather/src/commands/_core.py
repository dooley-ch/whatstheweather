# *******************************************************************************************
#  File:  _core.py
#
#  Created: 24-08-2022
#
#  History:
#  24-08-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['app']

import click
from ..ui import message


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.version_option(__version__, '--version', '-v')
def app(**kwargs) -> None:
    """
    This app produces current and daily weather reports for a given city.
    """
    pass


@app.group()
def location(**kwargs) -> None:
    """
    These commands are used to manage the locations
    """
    pass


@location.command("add")
def location_add() -> None:
    """
    This command adds a new location to the application
    """
    message("Location Add")


@location.command("edit")
@click.argument("location", type=click.STRING, required=True)
def location_edit(name: str) -> None:
    """
    This command adds a new location to the application

    NAME - The name of the location to edit
    """
    message("Location Edit")


@location.command("delete")
@click.argument("name", type=click.STRING, required=True)
def location_delete(name: str) -> None:
    """
    This command adds a new location to the application

    NAME - The name of the location to delete
    """
    message("Location Delete")


@location.command("list")
def location_list() -> None:
    """
    This command lists the locations in the application
    """
    message("Location List")


@app.group()
def weather(**kwargs) -> None:
    """
    These commands are used to obtain weather forecasts
    """
    pass


@weather.command("current")
@click.argument("name", type=click.STRING, required=True)
def weather_current(name: str) -> None:
    """
    This command obtains the current weather forecast

    NAME - The name of the location for the current weather
    """
    message("Current weather")


@weather.command("forecast")
@click.argument("name", type=click.STRING, required=True)
def weather_forecast(name: str) -> None:
    """
    This command obtains the weather forecast

    NAME - The name of the location for the forecast
    """
    message("Weather forcast")
