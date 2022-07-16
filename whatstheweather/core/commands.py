# *******************************************************************************************
#  File:  commands.py
#
#  Created: 05-07-2022
#
#  History:
#  05-07-2022: Initial version
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

import time
import re
from typing import NamedTuple
from pathlib import Path
import inquirer
from .logging import log_activity
from .support import find_folder
from .data import init_database, get_country_by_iso_3, get_country_by_iso_2, get_country_by_name, \
    get_state_by_name, get_state_by_code
from .config import get_api_key, save_api_key
import click
from .app_types import WeatherReportParams, UnitOfMeasure, Location, Country, State
from .open_weather_map import get_location, get_weather
from .reports import current_report, daily_report
from rich.console import Console

_console = Console()

_us_states = ["AL", "AK", "AZ", "AR", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
              "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND",
              "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "Other"]

pass_report_params = click.make_pass_decorator(WeatherReportParams)


class LocationCoordinates(NamedTuple):
    """
    Holds the coordinates of a given city
    """
    latitude: float
    longitude: float


def app_folder() -> Path:
    """
    Returns the location of the folder where the application's data is stored
    """
    return Path(click.get_app_dir('whatstheweather'))


# noinspection PyUnusedLocal
def _abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


def _get_location(city: str, country_code: str, api_key: str, state: str | None = None) -> LocationCoordinates | None:
    """
    Gets the location of a given city
    """
    if state == 'Other':
        state = None

    locs = get_location(city, country_code, api_key, state)
    if locs:
        if len(locs) == 1:
            return LocationCoordinates(locs[0].latitude, locs[0].longitude)

        loc_names = [str(loc) for loc in locs]
        loc_names.append('None of these')

        selected_loc = inquirer.list_input("Select location ", choices=loc_names)
        if selected_loc == 'None of these':
            return None

        regx = re.search('\((.+?)\)', selected_loc)
        if regx:
            found = regx.group(1)
            values = found.split(',')
            return LocationCoordinates(float(values[0]), float(values[1]))


def _get_state(database_path: Path, value: str) -> State | None:
    """
    Gets the details of a given state from the database
    """
    if len(value) == 2:
        return get_state_by_code(database_path, value)

    return get_state_by_name(database_path, value)


def _get_country(database_path: Path, value: str) -> Country | None:
    """
    Gets the details of a country from the database
    """
    if len(value) == 2:
        return get_country_by_iso_2(database_path, value)

    if len(value) == 3:
        return get_country_by_iso_3(database_path, value)

    return get_country_by_name(database_path, value)


@click.group
@click.version_option(__version__)
def app() -> None:
    """
    This app produces current and daily weather reports for a given city.
    """
    pass


@app.group(help='Configure the application')
def setup() -> None:
    """
    This command configures the application
    """
    pass


@setup.command
@click.option('--yes', is_flag=True, callback=_abort_if_false, expose_value=False,
              prompt='Are you sure you want to initialize the application?')
def init() -> None:
    """
    Initializes the app database with the country ISO codes
    """
    data_folder = find_folder('data')
    init_database(app_folder(), data_folder)
    log_activity('Application initialized')

    click.secho('Application initialized', fg='green')


@setup.command
@click.argument('value', required=True, type=str)
def key(value: str) -> None:
    """
    This command sets the OpenWeatherMap key value

    VALUE - A valid OpenWeatherMap key
    """
    save_api_key(app_folder(), value)
    click.secho('API Key saved', fg='green')


@app.group()
@click.pass_context
@click.option('--city', '-c', type=str, required=True, prompt='Enter city name ', help='The city to report on')
@click.option('--country', '-cty', type=str, required=True, prompt='Entry country name ',
              help='The country where the city is located')
@click.option('--unit', '-u', type=click.Choice(['standard', 'metric', 'imperial'], case_sensitive=False),
              required=False, default='standard', help='The reporting unit of measure')
@click.option('--state', '-s', type=click.Choice(_us_states, case_sensitive=False), required=False, default='Other',
              help='Needed for US cities')
def report(ctx: click.Context, city: str, country: str, unit: str, state: str) -> None:
    """
    This command generates a weather report
    """
    api_key = get_api_key(app_folder())

    ctry = _get_country(app_folder(), country)
    if not ctry:
        click.echo(f"Invalid country: {country}")
        raise click.Abort()

    state_record = State()
    if ctry.iso_2 == 'US':
        if state == 'Other':
            value = click.prompt('Enter state ', type=str)
            state_record = _get_state(app_folder(), value)
            if not state_record:
                click.echo(f"Invalid state: {value}")
                raise click.Abort()

    loc = _get_location(city, ctry.iso_2, api_key, state_record.code)

    if not loc:
        click.echo(f"Unable able to determine location for city: {city}")
        raise click.Abort()

    params: WeatherReportParams = WeatherReportParams(city, state_record.code, state_record.name, ctry.iso_2, ctry.name,
                                                      loc.longitude, loc.latitude, UnitOfMeasure(unit), api_key)
    ctx.obj = params


@report.command
@pass_report_params
def current(params: WeatherReportParams) -> None:
    """
     Generates the current weather report for a given city
    """
    loc = Location(params.city, params.state, params.country_code, params.longitude, params.latitude)
    weather_data = get_weather(loc, params.state, params.country, params.api_key, params.unit_of_measure)
    _console.print(current_report(weather_data))
    time.sleep(15)


@report.command
@pass_report_params
def daily(params: WeatherReportParams) -> None:
    """
     Generates the daily weather report for a given city
    """
    loc = Location(params.city, params.state, params.country_code, params.longitude, params.latitude)
    weather_data = get_weather(loc, params.state, params.country, params.api_key, params.unit_of_measure)
    _console.print(daily_report(weather_data))
    time.sleep(15)
