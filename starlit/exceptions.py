# -*- coding: utf-8 -*-
"""
    starlit.exceptions
    ~~~~~~~~~~

    The core exception classes for starlit

    :copyright: (c) 2018 by Musharraf Omer.
    :license: MIT, see LICENSE for more details.
"""

class StarlitException(Exception):
    """The base exception class for Starlit."""    
    def __init__(self, help_message=None):
        self.help_message = help_message


class StarlitConfigurationError(StarlitException):
    """Miss configuration of starlit"""


class BadlyFormattedFixture(StarlitException):
    """Raised when a fixture could not be decoded"""
