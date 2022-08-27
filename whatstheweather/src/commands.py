# *******************************************************************************************
#  File:  commands.py
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
from loguru import logger
from .ui import *
from .data import *
from .weather_service import get_forecast


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
@click.option('--count', '-c', default=10, type=int, required=False,
              help="Indicates the number of location entries to return")
def locations_add(count: int = 10) -> None:
    """
    This command adds a new location to the application
    """
    record = get_location(count)
    if record:
        if insert_location_record(record):
            success_message(f"New location added: {record.name}")
            logger.info(f"New location added: {record.name}")
        else:
            error_message(f"Failed to add new location, see log for details: {record.name}")


@location.command("edit")
@click.argument("name", type=click.STRING, required=True)
def locations_edit(name: str) -> None:
    """
    This command adds a new location to the application

    NAME - The name of the location to edit
    """
    record = get_location_record(name)
    if not location:
        system_message(f"No location found: {name}")
        return

    record = edit_location(record)
    if record:
        if update_location_record(record):
            success_message(f"Location record updated: {record.name}")
            logger.info(f"Location updated: {record.name}")
        else:
            warning_message(f"Failed to update location record, see log for details: {record.name}")


@location.command("delete")
@click.argument("name", type=click.STRING, required=True)
def locations_delete(name: str) -> None:
    """
    This command adds a new location to the application

    NAME - The name of the location to delete
    """
    if confirm_delete(name):
        if delete_location_record(name):
            success_message(f"Location deleted: {name}")
            logger.info(f"Location deleted: {name}")
        else:
            warning_message(f"Failed to delete location, record not found: {name}")


@location.command("list")
def locations_list() -> None:
    """
    This command lists the locations in the application
    """
    locations = all_locations()

    if locations:
        display_locations(locations)
    else:
        system_message("No locations found.")


@location.command("view")
@click.argument("name", type=click.STRING, required=True)
def locations_view(name: str) -> None:
    """
    This command adds a new location to the application

    NAME - The name of the location to view
    """
    record = get_location_record(name)
    if record:
        display_location_record(record)
    else:
        warning_message(f"Record not found, list locations to see records: {name}")


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
    record = get_location_record(name)
    if not record:
        system_message(f"There is no location defined with that name: {name}")
        return

    forecast = get_forecast(name, record.latitude, record.longitude, record.timezone)
    if not forecast:
        system_message(f"Unable to obtain a forecast for the location: {name}")
        return

    display_current_weather(forecast[0])


@weather.command("forecast")
@click.argument("name", type=click.STRING, required=True)
def weather_forecast(name: str) -> None:
    """
    This command obtains the weather forecast

    NAME - The name of the location for the forecast
    """
    record = get_location_record(name)
    if not record:
        system_message(f"There is no location defined with that name: {name}")
        return

    forecast = get_forecast(name, record.latitude, record.longitude, record.timezone)
    if not forecast:
        system_message(f"Unable to obtain a forecast for the location: {name}")
        return

    display_weather_forecast(forecast)
