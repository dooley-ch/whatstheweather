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

from .support import find_folder
from .data import init_database
from pprint import pprint

import click
from .app_types import WeatherReportParams, UnitOfMeasure

_us_states = ["AL", "AK", "AZ", "AR", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
              "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
              "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "Other"]


pass_report_params = click.make_pass_decorator(WeatherReportParams)


# noinspection PyUnusedLocal
def _abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


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
    app_folder = Path(click.get_app_dir('whatstheweather'))
    init_database(app_folder, data_folder)

@setup.command
@click.argument('value', required=True, type=str)
def key(value: str) -> None:
    """
    This command sets the OpenWeatherMap key value

    VALUE - A valid OpenWeatherMap key
    """
    print('Set API key')

    user_folder = click.get_app_dir('whatstheweather')
    print(user_folder)


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
    params: WeatherReportParams = WeatherReportParams(city, state, country, 0, 0,
                                                      UnitOfMeasure(unit), '6446a5397a0c3f38012e657b86f62be2')

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
