# *******************************************************************************************
#  File:  ui.py
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

__all__ = ['console', 'message', 'success_message', 'error_message', 'system_message', 'warning_message',
           'get_location', 'edit_location', 'confirm_message', 'confirm_delete', 'display_locations',
           'display_location_record', 'display_current_weather', 'display_weather_forecast']

from rich.console import Console
from rich.prompt import Confirm, Prompt, IntPrompt, FloatPrompt
from rich.text import Text
from rich.theme import Theme

from .model import Location, Locations, Forecast, Forecasts
from .weather_service import get_locations

theme = Theme({
    "normal_message": "bright_white on black",
    "error_message": "bright_red on black",
    "success_message": "light_green on black",
    "system_message": "bright_blue on black",
    "confirm_message": "bright_white on black",
    "warning_message": "orange3 on black",
    "table-style": "bright_white on black",
    "table-cell-style": "bright_white on black",
    "table-header-style": "bold bright_blue",
    "table-title-style": "bold bright_blue",
    "table-border-style": "bright_blue on black",
    "table-odd-row-style": "dark_sea_green3 on black",
    "table-even-row-style": "bright_blue on black",
})
console = Console(theme=theme)


def _message(value: str, text_style: str, clear: bool, pad: bool) -> None:
    """
    Internal function to display a message on the console
    """
    if clear:
        console.clear()
    if pad:
        console.line(1)

    msg = Text(value, style=text_style)
    console.print(msg)

    if pad:
        console.line(1)


# noinspection GrazieInspection
def message(value: str, clear: bool = False, pad: bool = True) -> None:
    """
    This function displays a normal message on the console

    :param value: the text to display
    :param clear: flag to indicate if the console should be cleared first
    :param pad: flag to indicate if the message should be preceded and succeeded by a blank line

    :return: None
    """
    _message(value, "normal_message", clear, pad)


# noinspection GrazieInspection
def error_message(value: str, clear: bool = False, pad: bool = True) -> None:
    """
    This function displays an error message on the console

    :param value: the text to display
    :param clear: flag to indicate if the console should be cleared first
    :param pad: flag to indicate if the message should be preceded and succeeded by a blank line

    :return: None
    """
    _message(value, "error_message", clear, pad)


def warning_message(value: str, clear: bool = False, pad: bool = True) -> None:
    """
    This function displays a warning message on the console

    :param value: the text to display
    :param clear: flag to indicate if the console should be cleared first
    :param pad: flag to indicate if the message should be preceded and succeeded by a blank line

    :return: None
    """
    _message(value, "warning_message", clear, pad)


# noinspection GrazieInspection
def success_message(value: str, clear: bool = False, pad: bool = True) -> None:
    """
    This function displays a success message on the console

    :param value: the text to display
    :param clear: flag to indicate if the console should be cleared first
    :param pad: flag to indicate if the message should be preceded and succeeded by a blank line

    :return: None
    """
    _message(value, "success_message", clear, pad)


# noinspection GrazieInspection
def system_message(value: str, clear: bool = False, pad: bool = True) -> None:
    """
    This function displays a system message on the console

    :param value: the text to display
    :param clear: flag to indicate if the console should be cleared first
    :param pad: flag to indicate if the message should be preceded and succeeded by a blank line

    :return: None
    """
    _message(value, "system_message", clear, pad)


# noinspection GrazieInspection
def confirm_message(value: str, clear: bool = False, pad: bool = True) -> bool:
    """
    This function ask the user to confirm or reject the execution of an action 
    
    :param value: the text to display
    :param clear: flag to indicate if the console should be cleared first
    :param pad: flag to indicate if the message should be preceded and succeeded by a blank line

    :return: None
    """
    if clear:
        console.clear()
    if pad:
        console.line(1)

    msg = Text(value, style="confirm_message")
    return Confirm.ask(msg)


def get_location(count: int) -> Location | None:
    """
    This function allows the user to select a new location
    """
    console.clear()

    name = Prompt.ask("Enter city/Town name")
    with console.status('Getting location information...'):
        locations = get_locations(name, count)
    if locations:
        console.clear()
        console.line(1)
        console.print(locations)
        console.line(1)

        choices = [str(i) for i in range(1, len(locations) + 1)]
        choice = IntPrompt.ask(f"Select the location (1..{len(choices)})", choices=choices, show_choices=False)

        location = locations[choice - 1]
        console.line(1)
        console.print(location)
        console.line(1)
        choice = Confirm.ask("Confirm adding this location to the application", default=True, show_default=True)
        if choice:
            return location
    else:
        system_message(f"No location information found for: {name}")
        return None

    system_message("No location record added")


def edit_location(record: Location) -> Location:
    """
    This function enables the user to edit a location record
    """
    console.clear()
    console.line(1)

    location = Prompt.ask("Enter city/Town name", default=record.name, show_default=True)
    latitude = FloatPrompt.ask("Enter latitude", default=str(record.latitude), show_default=True)
    longitude = FloatPrompt.ask("Enter longitude", default=str(record.longitude), show_default=True)
    region: str = Prompt.ask("Enter region name", default=record.region, show_default=True)
    country_code = Prompt.ask("Enter country code", default=record.country_code, show_default=True)
    country = Prompt.ask("Enter country name", default=record.country, show_default=True)
    timezone = Prompt.ask("Enter timezone", default=record.timezone, show_default=True)
    post_codes = Prompt.ask("Enter post codes, seperated by a coma", default=record.post_codes, show_default=True)

    # noinspection PyDataclass
    record = Location(record.name, location, latitude, longitude, region, country_code, country, timezone, post_codes)

    console.line(1)
    console.print(record)
    console.line(1)
    choice = Confirm.ask("Confirm the changes to the location record", default=True, show_default=True)
    if choice:
        return record


def confirm_delete(name: str, clear: bool = True, pad: bool = True) -> bool:
    """
    This function checks if the user wants to delete the given location

    :param name: The name of the location to delete
    :param clear: Flag to indicate if console should be cleared before displaying the confirmation message
    :param pad: Flag to indicate if message should be padded
    :return: True if successful otherwise false
    """
    return confirm_message(f"Are you sure you wish to delete the location: {name}")


def display_locations(records: Locations) -> None:
    """
    This function displays the list of locations

    :param records: The records to display
    :return: None
    """
    console.line(1)
    console.print(records)
    console.line(1)


def display_location_record(record: Location) -> None:
    """
    This function displays the given location record

    :param record: The record to display
    :return: None
    """
    console.line(1)
    console.print(record)
    console.line(1)


def display_current_weather(weather: Forecast) -> None:
    """
    This function displays the current weather forecast

    :param weather: The weather to display
    :return: None
    """
    console.line(1)
    console.print(weather)
    console.line(1)


def display_weather_forecast(weather: Forecasts) -> None:
    """
    This function displays the weather forecast

    :param weather: The weather to display
    :return: None
    """
    console.line(1)
    console.print(weather)
    console.line(1)
