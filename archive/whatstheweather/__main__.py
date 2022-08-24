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
import os
from pathlib import Path
import click
from core.logging import configure_logging, log_start, log_end
from core.commands import app


# noinspection PyBroadException
def exit_routine() -> None:
    """
    Logs the termination of the application
    """
    try:
        log_end()
    except:
        click.secho('Failed to log application exit!', fg='red')


def main() -> None:
    """
    The application entry point
    """
    # Set the working folder
    working_folder: Path = Path(__file__).parent
    os.chdir(working_folder)

    # Set up the exit routine
    atexit.register(exit_routine)

    # Configure logging
    print(click.get_app_dir('whatstheweather'))
    configure_logging(Path(click.get_app_dir('whatstheweather')))
    log_start()

    # Process the commands
    app()


if __name__ == '__main__':
    main()
