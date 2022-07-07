# *******************************************************************************************
#  File:  __main__.py
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


from core.commands import app

def main() -> None:
    app()


if __name__ == '__main__':
    main()
