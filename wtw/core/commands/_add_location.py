# *******************************************************************************************
#  File:  _add_location.py
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

__all__ = ['add']

import rich.prompt
import rich.text
from .. import ui
from .. import weather_service
from .. import data
from .. import model


def add() -> model.Result:
    """
    This function handles the adding of a location
    """
    ui.start_feature('Add Location')

    name = rich.prompt.Prompt.ask(rich.text.Text("\tEnter city/Town name", tab_size=4), console=ui.console)

    if len(name) == 0:
        ui.system_message('Add location aborted.')
        return model.Result.NoOperation

    name = name.title()

    ui.console.line(1)
    with ui.console.status('Download locations...'):
        locations = weather_service.get_locations(name)

    if locations is None:
        ui.system_message('No locations found, please try again.')
        return model.Result.NoOperation

    location = locations[0]
    if len(locations) > 1:
        ui.console.line(1)
        ui.console.print(locations)
        ui.console.line(1)
        choices = [str(i) for i in range(0, len(locations))]
        choice = rich.prompt.IntPrompt.ask(rich.text.Text(f"\tSelect the location (0..{len(choices) - 1})", tab_size=4),
                                           choices=choices, show_choices=False)
        location = locations[choice]
    else:
        location = locations[0]

    ui.console.line(1)
    ui.console.print(location)
    action = ui.confirm_message('Are you sure you want to add the new location', default=False)

    if not action:
        ui.system_message('Add location aborted.')
        return model.Result.NoOperation

    if not data.insert_location_record(location):
        ui.system_message('A location with this name already exists.')
        return model.Result.NoOperation

    ui.end_feature()

    return model.Result.Success
