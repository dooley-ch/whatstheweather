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
