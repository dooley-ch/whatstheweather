# *******************************************************************************************
#  File:  weather_service_test.py
#
#  Created: 25-08-2022
#
#  History:
#  25-08-2022: Initial version
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

import whatstheweather.src.weather_service as service


def test_get_locations_langenthal() -> None:
    locations = service.get_locations('Langenthal')
    assert len(locations) >= 8


def test_get_locations_city_of_london() -> None:
    locations = service.get_locations('City of London')
    assert len(locations) == 1


def test_get_forecast_langenthal() -> None:
    forecasts = service.get_forecast(47.2116019, 7.788786, 'Europe/Berlin')
    assert len(forecasts) == 7


def test_get_forecast_city_of_london() -> None:
    forecasts = service.get_forecast(51.5156177, -0.0919983, 'Europe/Berlin')
    assert len(forecasts) == 7
