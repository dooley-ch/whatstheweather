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

__all__ = ['console', 'message', 'success_message', 'error_message', 'system_message']

from rich.console import Console
from rich.theme import Theme
from rich.text import Text

theme = Theme({
    "normal_message" : "bright_white on black",
    "error_message" : "bright_red on black",
    "success_message" : "light_green on black",
    "system_message" : "bright_blue on black"
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


def message(value: str, clear: bool = False, pad: bool = True) -> None:
    """
    This function displays a normal message on the console

    :param value: the text to display
    :param clear: flag to indicate if the console should be cleared first
    :param pad: flag to indicate if the message should be preceded and succeeded by a blank line

    :return: None
    """
    _message(value, "normal_message", clear, pad)


def error_message(value: str, clear: bool = False, pad: bool = True) -> None:
    """
    This function displays an error message on the console

    :param value: the text to display
    :param clear: flag to indicate if the console should be cleared first
    :param pad: flag to indicate if the message should be preceded and succeeded by a blank line

    :return: None
    """
    _message(value, "error_message", clear, pad)


def success_message(value: str, clear: bool = False, pad: bool = True) -> None:
    """
    This function displays a success message on the console

    :param value: the text to display
    :param clear: flag to indicate if the console should be cleared first
    :param pad: flag to indicate if the message should be preceded and succeeded by a blank line

    :return: None
    """
    _message(value, "success_message", clear, pad)


def system_message(value: str, clear: bool = False, pad: bool = True) -> None:
    """
    This function displays a system message on the console

    :param value: the text to display
    :param clear: flag to indicate if the console should be cleared first
    :param pad: flag to indicate if the message should be preceded and succeeded by a blank line

    :return: None
    """
    _message(value, "system_message", clear, pad)
