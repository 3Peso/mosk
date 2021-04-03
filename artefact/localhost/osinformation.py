"""
mosk localhost module for classes collecting os information.
"""

__author__ = '3Peso'
__all__ = ['OSName', 'OSVersion', 'OSTimezone']

import platform
import sys
from datetime import datetime

from baseclasses.artefact import MacArtefact, ArtefactBase
from businesslogic.support import run_terminal_command


METHOD_KEY = 'CollectionMethod'
DESCRIPTION_KEY = 'Description'
LOOKUP_KEY = 'lookup'
VERSION_NUMBER_INDEX = 0

_platform_lookup = {
    'darwin': {
        LOOKUP_KEY: {
            # TODO Refactor in a manor, so that only the important parts are used to determine the os name.
            # Example: For BigSur only the 11 is important. For Sierra only 10.12 is important.
            # TODO Try to find a way to collect OS information online
            '10.10': 'Yosemite',
            '10.11': 'El Capitan',
            '10.12': 'Sierra',
            '10.13': 'High Sierra',
            '10.14': 'Mojave',
            '10.15': 'Catalina',
            '11.0': 'BigSur',
            '11.1': 'BigSur',
            '11.2': 'BigSur',
            '11.2.1': 'BigSur',
            '11.2.2': 'BigSur',
            '11.2.3': 'BigSur'
        }
    }
}


class OSName(MacArtefact):
    """
    Tries to look up the installed OS name.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        if sys.platform == 'darwin':
            platformversion = platform.mac_ver()[VERSION_NUMBER_INDEX]
            try:
                self.data = _platform_lookup[sys.platform][LOOKUP_KEY][platformversion]
            except KeyError:
                self.data = f"Cannot collect OS name for platform version '{platformversion}'"


class OSVersion(MacArtefact):
    """
    Tries to retrieve the OS version number.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        if sys.platform == 'darwin':
            self.data = platform.mac_ver()[VERSION_NUMBER_INDEX]


class OSTimezone(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        self.data = datetime.now().astimezone().tzname()


class SudoVersion(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._supportedsystem = ('Darwin', 'Linux')

    def _collect(self):
        self.data = run_terminal_command(['sudo', '-V'])


class OSPlatform(ArtefactBase):
    """Collects the platform on which this script is running on."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        self.data = platform.system()
