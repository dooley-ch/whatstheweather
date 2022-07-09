# *******************************************************************************************
#  File:  logging_test.py
#
#  Created: 09-07-2022
#
#  History:
#  09-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

from pathlib import Path
from loguru import logger
import whatstheweather.core.logging as logging


class TestLogging:
    def test_write_activity(self, init_logger) -> None:
        activity_file = init_logger.joinpath("activity.log")

        logging.log_start()
        logging.log_activity('First activity message')
        logging.log_activity('This is a long message, repeat. This is a long message, repeat. This is a long message, repeat.')
        logging.log_activity('Long activity message')
        logging.log_end()

        assert activity_file.exists()
        assert activity_file.stat().st_size == 593

    def test_write_error(self, init_logger) -> None:
        errors_file = init_logger.joinpath("errors.log")

        logger.error('First Error Message')
        logger.error('Second Error Message')
        logger.error('Third Error Message')
        logger.error('Fourth Error Message')
        logger.error('Fifth Error Message')

        assert errors_file.exists()
        assert errors_file.stat().st_size == 642

    def test_write_core(self, init_logger) -> None:
        core_file = init_logger.joinpath("core.log")

        logger.info('This is an info message')
        logger.warning('This is a warning message')
        logger.error('This is an error message')
        logger.critical('This is a critical message')

        assert core_file.exists()
        assert core_file.stat().st_size == 1410
