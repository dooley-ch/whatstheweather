# *******************************************************************************************
#  File:  logging.py
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

__all__ = ['configure_logging', 'log_start', 'log_end', 'log_activity']

from pathlib import Path
from loguru import logger


class ActivityFileFormatter:
    def __init__(self):
        self._default_format = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {function: ^15} | {file: ^15} | {line: >3} " \
                               "" \
                               "| {message} \n"
        self._line_format = "========================================== {time:YYYY-MM-DD HH:mm:ss} " \
                            "=============================================== \n"

    def format(self, record):
        if 'line' in record["extra"]:
            return self._line_format

        return self._default_format


def configure_logging(app_folder: Path):
    file_format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {function: ^15} | {file: ^15} | {line: >3} | {" \
                       "message}"

    core_file = app_folder.joinpath("core.log")
    errors_file = app_folder.joinpath("errors.log")
    activity_file = app_folder.joinpath("activity.log")

    activity_formatter = ActivityFileFormatter()

    logger.remove()

    logger.level("LINE", no=60, color="<white>")

    logger.add(core_file, rotation='1 day', retention='5 days', compression='zip', level='INFO',
               backtrace=True, diagnose=True, format=file_format)
    logger.add(errors_file, rotation='1 day', retention='5 days', compression='zip', level='ERROR',
               backtrace=True, diagnose=True, format=file_format)
    logger.add(activity_file, rotation='1 day', retention='5 days', compression='zip', level='SUCCESS',
               filter=lambda record: "activity" in record["extra"], format=activity_formatter.format)


def log_start():
    logger.bind(activity=True, line=True).log("LINE", 'Start')


def log_end():
    logger.bind(activity=True, line=True).log("LINE", 'End')


def log_activity(message: str) -> None:
    logger.bind(activity=True).success(message)
