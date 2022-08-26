# *******************************************************************************************
#  File:  __main__.py
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

import atexit

from loguru import logger
from rich.traceback import install

from src.commands import app
from src.support import configure_logging, app_folder
from src.ui import system_message


# noinspection PyBroadException
def exit_routine() -> None:
    """
    Logs the termination of the application
    """
    try:
        logger.info("*** Application Ended ***")
    except:
        system_message('Failed to log application exit!')


def main():
    # Configure traceback support
    install(show_locals=True, max_frames=5)

    # Configure logging
    configure_logging(app_folder())

    # Setup exit callback
    atexit.register(exit_routine)

    # Run application
    logger.info("*** Application Started ***")
    app()


if __name__ == '__main__':
    main()
