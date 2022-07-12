# *******************************************************************************************
#  File:  reports_test.py
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

from rich.console import Console
import whatstheweather.core.reports as rpts


def test_current_report_balla(weather_data_balla) -> None:
    report = rpts.current_report(weather_data_balla)

    console = Console()
    assert report
    console.print(report)


def test_current_report_new_york(weather_data_new_york) -> None:
    report = rpts.current_report(weather_data_new_york)
    assert report

    console = Console()
    console.print(report)


def test_daily_report(weather_data_balla) -> None:
    report = rpts.daily_report(weather_data_balla)
    assert report
