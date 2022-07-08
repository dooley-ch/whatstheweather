# *******************************************************************************************
#  File:  config.py
#
#  Created: 08-07-2022
#
#  History:
#  08-07-2022: Initial version
#
# *******************************************************************************************

__author__ = "James Dooley"
__contact__ = "james@developernotes.org"
__copyright__ = "Copyright (c) 2022 James Dooley <james@dooley.ch>"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "James Dooley"
__status__ = "Production"

__all__ = ['save_api_key', 'get_api_key']

import configparser
from pathlib import Path


def _get_config_file(app_folder: Path) -> Path:
    """
    Returns the database file name
    """
    return app_folder.joinpath('whatstheweather.cfg')


def get_api_key(app_folder: Path) -> str | None:
    """
    This function returns the OpenWeatherMap API key
    """
    cfg_file = _get_config_file(app_folder)
    if not cfg_file.exists():
        raise FileNotFoundError(f"Config File: {cfg_file}")

    config = configparser.ConfigParser()
    config.read(cfg_file)

    return config['OpenWeatherMap']["api_key"]


def save_api_key(app_folder: Path, value: str) -> None:
    """
    This function stores the given OpenWeatherMap API key
    """
    cfg_file = _get_config_file(app_folder)
    if cfg_file.exists():
        cfg_file.unlink()

    config = configparser.ConfigParser()
    config['OpenWeatherMap'] = {"api_key": value}

    with cfg_file.open('w') as file:
        config.write(file)
