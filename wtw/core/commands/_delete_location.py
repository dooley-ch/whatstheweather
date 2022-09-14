# *******************************************************************************************
#  File:  _delete_location.py
#
#  Created: 14-09-2022
#
#  History:
#  14-09-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['delete']

from .. import model
from .. import ui
from .. import data


def delete(location: str) -> model.Result:
    """
    This function deletes a given location
    """
    ui.start_feature('Add Location')

    location = location.title()
    record = data.get_location_record(location)

    if record is None:
        ui.console.line(1)
        ui.system_message(f"The location ({location}) was not found in the database")
        ui.console.line(1)
        return model.Result.NoOperation

    ui.end_feature()

    if data.delete_location_record(location):
        return model.Result.Success

    return model.Result.Fail
