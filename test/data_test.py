# *******************************************************************************************
#  File:  data_test.py
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

from pathlib import Path
import whatstheweather.core.data as data


class TestData:
    def test_init_database_valid(self, app_folder, data_folder: Path) -> None:
        data.init_database(app_folder, data_folder)

        data_file = app_folder.joinpath('data.json')
        assert data_file.exists()


class TestSateData:
    def test_get_state_by_name(self, app_folder) -> None:
        state = data.get_state_by_name(app_folder, 'Texas')
        assert state.code == 'TX'

        country = data.get_state_by_name(app_folder, 'Oregon')
        assert country.code == 'OR'

    def test_get_state_by_code(self, app_folder) -> None:
        state = data.get_state_by_code(app_folder, 'TX')
        assert state.name == 'Texas'

        country = data.get_state_by_code(app_folder, 'OR')
        assert country.name == 'Oregon'

    def test_is_valid_state(self, app_folder) -> None:
        assert data.is_valid_state(app_folder, 'Oregon')
        assert not data.is_valid_state(app_folder, 'No State')

    def test_is_valid_state_code(self, app_folder) -> None:
        result = data.is_valid_state_code(app_folder, 'OR')
        assert result

        result = data.is_valid_state_code(app_folder, 'XX')
        assert not result


class TestCountryData:
    def test_get_by_name(self, app_folder) -> None:
        country = data.get_country_by_name(app_folder, 'Switzerland')
        assert country.iso_2 == 'CH'

        country = data.get_country_by_name(app_folder, 'United States of America')
        assert country.iso_2 == 'US'

    def test_get_iso_3(self, app_folder) -> None:
        country = data.get_country_by_iso_3(app_folder, 'CHE')
        assert country.name == 'Switzerland'

        country = data.get_country_by_iso_3(app_folder, 'USA')
        assert country.name == 'United States of America'

    def test_get_iso_2(self, app_folder) -> None:
        country = data.get_country_by_iso_2(app_folder, 'CH')
        assert country.name == 'Switzerland'

        country = data.get_country_by_iso_2(app_folder, 'US')
        assert country.name == 'United States of America'

    def test_is_valid_name(self, app_folder) -> None:
        assert data.is_valid_country_name(app_folder, 'Switzerland')
        assert data.is_valid_country_name(app_folder, 'United States of America')

    def test_is_valid_iso_2(self, app_folder) -> None:
        assert data.is_valid_iso_2_country_code(app_folder, 'CH')
        assert data.is_valid_iso_2_country_code(app_folder, 'US')

    def test_is_valid_iso_3(self, app_folder) -> None:
        assert data.is_valid_iso_3_country_code(app_folder, 'CHE')
        assert data.is_valid_iso_3_country_code(app_folder, 'USA')
