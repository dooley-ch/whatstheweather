# *******************************************************************************************
#  File:  support.py
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

__all__ = ['app_folder', 'configure_logging']

from pathlib import Path
import click
from loguru import logger


def app_folder() -> Path:
    """
    Returns the location of the folder where the application's data is stored
    """
    return Path(click.get_app_dir('whatstheweather'))


def configure_logging(application_folder: Path):
    """
    Configures logging for the application
    """
    file_format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {function: ^15} | {file: ^15} | {line: >3} | {" \
                       "message}"

    log_file = application_folder.joinpath("app.log")

    logger.remove()

    logger.add(log_file, rotation='1 day', retention='5 days', compression='zip', level='INFO',
               backtrace=True, diagnose=True, format=file_format)
