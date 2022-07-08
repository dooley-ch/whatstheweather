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


@pytest.fixture(scope="session")
def app_folder() -> Path:
    return Path(__file__).parent.joinpath('user_folder')


@pytest.fixture(scope="session")
def data_folder() -> Path:
    return Path(__file__).parent.parent.joinpath('whatstheweather', 'data')
