# *******************************************************************************************
#  File:  conftest.py
#
#  Created: 30-05-2022
#
#  Copyright (c) 2022 James Dooley <james@dooley.ch>
#
#  History:
#  30-05-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

from pathlib import Path
import pytest
import whatstheweather.core.logging as logging
import whatstheweather.core.app_types as types
import whatstheweather.core.open_weather_map as owm


@pytest.fixture(scope="session")
def app_folder() -> Path:
    return Path(__file__).parent.joinpath('user_folder')


@pytest.fixture(scope="session")
def data_folder() -> Path:
    return Path(__file__).parent.parent.joinpath('whatstheweather', 'data')


@pytest.fixture(scope="session")
def open_weather_map_key() -> str:
    return '6446a5397a0c3f38012e657b86f62be2'


@pytest.fixture(scope="session")
def init_logger() -> Path:
    logs_folder = Path(__file__).parent.joinpath('user_folder')

    core_file = logs_folder.joinpath("core.log")
    if core_file.exists():
        core_file.unlink()

    errors_file = logs_folder.joinpath("errors.log")
    if errors_file.exists():
        errors_file.unlink()

    activity_file = logs_folder.joinpath("activity.log")
    if activity_file.exists():
        activity_file.unlink()

    logging.configure_logging(logs_folder)

    return logs_folder


@pytest.fixture(scope="session")
def weather_data_balla(open_weather_map_key) -> types.WeatherData:
    locations = owm.get_location('Balla', 'IE', open_weather_map_key)
    assert len(locations) == 3
    item = locations[0]

    return owm.get_weather(item, 'Other', 'Ireland', open_weather_map_key)


@pytest.fixture(scope="session")
def weather_data_new_york(open_weather_map_key) -> types.WeatherData:
    locations = owm.get_location('New York', 'US', open_weather_map_key, 'NY')
    assert len(locations) == 1
    item = locations[0]

    return owm.get_weather(item, 'New York', 'United States of America', open_weather_map_key)
