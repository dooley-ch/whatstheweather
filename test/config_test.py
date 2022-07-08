# *******************************************************************************************
#  File:  config_test.py
#
#  Created: 08-07-2022
#
#  History:
#  08-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

import whatstheweather.core.config as cfg


class TestConfig:
    def test_save_key(self, app_folder) -> None:
        cfg.save_api_key(app_folder, '999-999')
        config_file = app_folder.joinpath('whatstheweather.cfg')
        assert config_file.exists()

    def test_get_key(self, app_folder) -> None:
        key = cfg.get_api_key(app_folder)
        assert key == '999-999'
