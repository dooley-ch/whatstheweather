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

from pathlib import Path
from .logging import log_activity
from .support import find_folder
from .data import init_database, is_valid_iso_2_country_code, is_valid_iso_3_country_code, is_valid_country_name, \
    get_country_by_iso_3, get_country_by_name, is_valid_state_code, get_state_by_name
from .config import get_api_key, save_api_key
from pprint import pprint
import click
from .app_types import WeatherReportParams, UnitOfMeasure, Location
from .open_weather_map import get_location, get_weather


_us_states = ["AL", "AK", "AZ", "AR", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY",
              "LA",
              "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH",
              "OK",
              "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "Other"]

pass_report_params = click.make_pass_decorator(WeatherReportParams)


def app_folder() -> Path:
    return Path(click.get_app_dir('whatstheweather'))


# noinspection PyUnusedLocal
def _abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


def _get_location(city: str, country_code: str, key: str, state: str | None = None) -> Location | None:
    if state == 'Other':
        state = None

    locs = get_location(city, country_code, key, state)
    if locs:
        if len(locs) == 1:
            return locs[0]


def _get_state_code(database_path: Path, value: str) -> str | None:
    if len(value) == 2:
        if is_valid_state_code(database_path, value):
            return value
        else:
            return None

    state = get_state_by_name(value)
    if state:
        return state.code


def _get_country_code(database_path: Path, value: str) -> str | None:
    if len(value) == 2:
        if is_valid_iso_2_country_code(database_path, value):
            return value
        else:
            return None

    if len(value) == 3:
        if is_valid_iso_3_country_code(database_path, value):
            data = get_country_by_iso_3(database_path, value)
            return data.iso_2
        else:
            return None

    if is_valid_country_name(database_path, value):
        data = get_country_by_name(database_path, value)
        return data.iso_2


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

    ctry = _get_country_code(app_folder(), country)
    if not ctry:
        click.echo(f"Invalid country: {country}")
        raise click.Abort()

    st = 'Other'
    if ctry == 'US':
        if state == 'Other':
            state = click.prompt('Enter state ', type=str)
            st = _get_state_code(app_folder(), state)
            if not st:
                click.echo(f"Invalid state: {state}")
                raise click.Abort()

    loc: Location = _get_location(city, ctry, api_key, st)
    if not loc:
        click.echo(f"Unable able to determine location for city: {city}")
        raise click.Abort()

    params: WeatherReportParams = WeatherReportParams(city, st, ctry, loc.longitude, loc.latitude,
                                                      UnitOfMeasure(unit), api_key)
    ctx.obj = params


@report.command
@pass_report_params
def current(params) -> None:
    """
     Generates the current weather report for a given city
    """
    pprint(params)


@report.command
@pass_report_params
def daily(params) -> None:
    """
     Generates the daily weather report for a given city
    """
    pprint(params)
