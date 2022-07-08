# *******************************************************************************************
#  File:  setup.py
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

from setuptools import setup, find_packages

setup(
    name='whatstheweather',
    version='1.0.0',
    packages=find_packages(exclude=('test',)),
    package_data={
      'whatstheweather': ['data/*.csv'],
    },
    include_package_data=True,
    install_requires=[
        'Click',
        'Attrs',
        'Pendulum',
        'TinyDB'
    ],
    entry_points={
        'console_scripts': [
            'whatstheweather = whatstheweather.core.commands:app',
        ],
    },
)
