# *******************************************************************************************
#  File:  utils.py
#
#  Created: 13-09-2022
#
#  History:
#  13-09-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['app_folder', 'config_logging']

import pathlib
import click
import loguru


def app_folder() -> pathlib.Path:
    """
    Returns the location of the folder where the application's data is stored
    """
    return pathlib.Path(click.get_app_dir('wtw'))


def config_logging():
    """
    Configures logging for the application
    """
    file_format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {function: ^15} | {file: ^15} | {line: >3} | {" \
                       "message}"

    log_file = app_folder().joinpath("app.log")

    loguru.logger.remove()

    loguru.logger.add(log_file, rotation='1 day', retention='5 days', compression='zip', level='INFO',
                      backtrace=True, diagnose=True, format=file_format)
