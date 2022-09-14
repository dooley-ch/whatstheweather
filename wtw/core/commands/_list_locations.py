# *******************************************************************************************
#  File:  _list_locations.py
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

__all__ = ['list']

from .. import ui
from .. import data


def list() -> None:
    """
    Display the list of locations
    """
    ui.start_feature('List Locations')
    locations = data.all_locations()

    ui.console.line(1)
    ui.console.print(locations)

    ui.end_feature()
