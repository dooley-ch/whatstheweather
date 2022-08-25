# *******************************************************************************************
#  File:  conftest.py
#
#  Created: 25-08-2022
#
#  History:
#  25-08-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = []

from pathlib import Path
import pytest


@pytest.fixture()
def db_file_name() -> Path:
    db_file = Path(__file__).parent.joinpath('data', 'data.sqlite')
    if db_file.exists():
        db_file.unlink()

    return db_file
