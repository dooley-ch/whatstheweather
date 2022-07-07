# *******************************************************************************************
#  File:  data_test.py
#
#  Created: 07-07-2022
#
#  History:
#  07-07-2022: Initial version
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
import whatstheweather.core.data as data


class TestData:
    def test_init_database_valid(self, user_folder: Path, data_folder: Path) -> None:
        assert data.init_database(user_folder, data_folder)
