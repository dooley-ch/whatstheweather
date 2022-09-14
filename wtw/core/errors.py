# *******************************************************************************************
#  File:  errors.py
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

__all__ = ['DuplicateRecordError', 'RecordNotFoundError']


class DuplicateRecordError(Exception):
    """
    Raised when the user tries to insert the same record in the table more than once
    """
    pass


class RecordNotFoundError(Exception):
    """
    Raised when a record can't be found in the database
    """
    pass
