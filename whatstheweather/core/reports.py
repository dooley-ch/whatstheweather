# *******************************************************************************************
#  File:  reports.py
#
#  Created: 11-07-2022
#
#  History:
#  11-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['current_report', 'daily_report']

from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from .app_types import WeatherData, Report, UnitOfMeasure

console = Console()


class _ReportPanelBase:
    """
    This class provides common routines for building weather reports
    """
    _data: WeatherData

    def __init__(self, data: WeatherData) -> None:
        """
        Initializes the instance with the reporting data
        """
        self._data = data

    # noinspection PyMethodMayBeStatic
    def _format_temp(self, value: float, unit_of_measure: UnitOfMeasure) -> str:
        match unit_of_measure:
            case UnitOfMeasure.Metric: return f"{value}°C"
            case UnitOfMeasure.Imperial: return f"{value}°F"
            case _: return f"{value}°K"

    # noinspection PyMethodMayBeStatic
    def _format_percentage(self, value: int) -> str:
        """
        This method formats percentage values
        """
        return f"{value}%"

    # noinspection PyMethodMayBeStatic
    def _format_visibility(self, value: int) -> str:
        if value < 1000:
            return f"{value}m"
        return f"{round(value / 1000, 2)}Km"

    # noinspection PyMethodMayBeStatic
    def _format_wind_direction(self, value: float) -> str:
        return f"{value}°"

    # noinspection PyMethodMayBeStatic
    def _format_wind_speed(self, value: float, unit_of_measure: UnitOfMeasure) -> str:
        if unit_of_measure == UnitOfMeasure.Imperial:
            return f"{value} miles/hour"
        return f"{value} metre/sec"

    # noinspection PyMethodMayBeStatic
    def _format_pressure(self, value: float) -> str:
        return f"{value} hPa"


class _CurrentReportPanel(_ReportPanelBase):
    """
    This class builds the current report panel
    """
    def __rich__(self) -> Panel:
        current_weather = self._data.current_weather
        uom = self._data.unit_of_measure

        grid = Table.grid(padding=1)
        grid.add_column()
        grid.add_column()
        grid.add_column(justify='right')
        grid.add_column(justify='left')

        grid.add_row('Temperature:', self._format_temp(current_weather.temp, uom))
        grid.add_row('Feels Like:', self._format_temp(current_weather.feels_like, uom))
        grid.add_row('Sunrise:', current_weather.sunrise.to_datetime_string())
        grid.add_row('Sunset:', current_weather.sunset.to_datetime_string())
        grid.add_row('pressure:', self._format_pressure(current_weather.pressure))
        grid.add_row('humidity:', self._format_percentage(current_weather.humidity))
        grid.add_row('clouds:', self._format_percentage(current_weather.clouds))
        grid.add_row('Visibility:', self._format_visibility(current_weather.visibility))
        grid.add_row('Weather:', current_weather.weather.description)
        grid.add_row('Wind Direction:', self._format_wind_direction(current_weather.wind_deg))
        grid.add_row('Wind Speed:', self._format_wind_speed(current_weather.wind_speed, uom))

        return Panel(grid, title='Current Weather', style="yellow on black")


# noinspection PyMethodMayBeStatic
class _Header:
    """
    Display the report header with clock.
    """

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)

        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]What's The Weather - 1.0.0[/b]",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")


# noinspection PyMethodMayBeStatic
class _Footer:
    """
    Displays the report footer with blog link
    """

    def __rich__(self) -> Panel:
        grid = Table.grid(padding=1, expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_row(
            "Check out the blog (ctrl + click to open): [u green "
            "link=https://www.developernotes.org]https://www.developernotes.org",
        )
        return Panel(grid, style="white on blue")


class _Location:
    """
    Displays the location in the left panel
    """
    _city: str
    _state: str
    _country: str
    _longitude: float
    _latitude: float

    def __init__(self, city: str, state: str, country: str, longitude: float, latitude: float) -> None:
        if city.startswith('='):
            city = city[1:]

        self._city = city
        self._state = state
        self._country = country
        self._longitude = longitude
        self._latitude = latitude

    def __rich__(self) -> Panel:
        grid = Table.grid(padding=1, expand=True)
        grid.add_column(justify='right')
        grid.add_column(justify='left')
        grid.add_row("City: ", self._city)
        if self._state != 'Other':
            grid.add_row("State: ", self._state)
        grid.add_row("Country: ", self._country)
        grid.add_row("coordinates: ", f"{self._latitude}°, {self._longitude}°")

        return Panel(grid, title='Location', style="yellow on blue")


def _get_report_layout() -> Layout:
    """
    This function builds the basic report layout
    :return:
    """
    layout = Layout(name="root")

    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )

    layout["main"].split_row(
        Layout(name="location"),
        Layout(name="body", ratio=2, minimum_size=60),
    )

    layout["header"].update(_Header())
    layout["footer"].update(_Footer())

    return layout


def current_report(data: WeatherData) -> Report:
    """
    This function creates the current weather report
    """
    layout = _get_report_layout()
    layout["location"].update(_Location(data.city, data.state, data.country, data.longitude, data.latitude))
    layout["body"].update(_CurrentReportPanel(data))

    return Report(layout)


def daily_report(data: WeatherData) -> Report:
    """
    This function creates the daily weather report
    """
    pass