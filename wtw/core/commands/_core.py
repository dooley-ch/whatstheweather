# *******************************************************************************************
#  File:  _core.py
#
#  Created: 13-09-2022
#
#  History:
#  13-09-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['main']

import atexit
import rich.traceback
import click
import loguru
from .. import utils
from .. import ui
from .. import model
from . import _add_location
from . import _list_locations
from . import _delete_location
from . import _weather


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.version_option(__version__, '--version', '-v')
def app(**kwargs) -> None:
    """
    This app produces current and daily weather reports for a given city.
    """
    pass


@app.command('current')
@click.pass_context
@click.argument("location", type=click.STRING, required=True)
@loguru.logger.catch(reraise=True, message='Logged while getting current weather')
def current_weather(ctx: click.Context, location: str) -> None:
    """
    Displays the current weather

    LOCATION The weather location
    """
    _weather.current(location)


@app.command('forecast')
@click.pass_context
@click.argument("location", type=click.STRING, required=True)
@loguru.logger.catch(reraise=True, message='Logged while getting forecast')
def forecast_weather(ctx: click.Context, location: str) -> None:
    """
    Displays the weather forecast

    LOCATION The forecast location
    """
    _weather.forecast(location)


@app.group('location')
def loc(**kwargs) -> None:
    """
    Manages the reporting locations.
    """
    pass


@loc.command('list')
@click.pass_context
def location_list(ctx: click.Context) -> None:
    """
    Displays the weather forecast

    LOCATION The forecast location
    """
    _list_locations.list()
    ctx.exit(0)


@loc.command('add')
@click.pass_context
@loguru.logger.catch(reraise=True, message='Logged while adding location')
def location_add(ctx: click.Context) -> None:
    """
    Adds a new location
    """
    result = _add_location.add()
    if result == model.Result.Success:
        ui.success_message("Location added successfully.")
        ctx.exit(0)
    elif result == model.Result.Fail:
        ui.error_message("Failed to added location, see log for details.")
        ctx.exit(1)
    else:
        ctx.exit(0)


@loc.command('delete')
@click.pass_context
@click.argument("location", type=click.STRING, required=True)
@loguru.logger.catch(reraise=True, message='Logged while deleting location')
def location_delete(ctx: click.Context, location: str) -> None:
    """
    Delete the given location

    LOCATION The location to delete
    """
    result = _delete_location.delete(location)
    if result == model.Result.Success:
        ui.success_message("Location deleted successfully.")
        ctx.exit(0)
    elif result == model.Result.Fail:
        ui.error_message("Failed to delete location, see log for details.")
        ctx.exit(1)
    else:
        ctx.exit(0)


# noinspection PyBroadException
def exit_routine() -> None:
    """
    Logs the termination of the application
    """
    try:
        loguru.logger.info("*** Application Ended ***")
    except:
        ui.system_message('Failed to log application exit!')


def main():
    """
    The application entry point
    """
    # Configure traceback support
    rich.traceback.install(show_locals=True, max_frames=5)

    utils.config_logging()

    # Setup exit callback - logs the exit of the application
    atexit.register(exit_routine)

    # Run application
    loguru.logger.info("*** Application Started ***")
    app()
