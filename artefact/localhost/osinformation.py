"""
mosk localhost module for classes collecting os information.
"""

__author__ = '3Peso'
__all__ = ['OSName', 'OSVersion', 'OSTimezone']

import logging
import platform
import sys
import re
from datetime import datetime

from baseclasses.artefact import MacArtefact, ArtefactBase
from businesslogic.support import run_terminal_command
from businesslogic.errors import UnknownVersionStringError


METHOD_KEY = 'CollectionMethod'
DESCRIPTION_KEY = 'Description'
LOOKUP_KEY = 'lookup'
VERSION_NUMBER_INDEX = 0

_platform_lookup: dict = {
    'darwin': {
        LOOKUP_KEY: {
            '10': {
                '10': 'Yosemite',
                '11': 'El Capitan',
                '12': 'Sierra',
                '13': 'High Sierra',
                '14': 'Mojave',
                '15': 'Catalina'
            },
            '11': 'BigSur',
            '12': 'Monterey'
        }
    }
}


class OSName(MacArtefact):
    """
    Tries to look up the installed OS name.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        logger = logging.getLogger(__name__)
        if sys.platform == 'darwin':
            platformversion = platform.mac_ver()[VERSION_NUMBER_INDEX]
            try:
                self._verify_version_string(platformversion)
                version_tuple = platformversion.split('.')
                tmp = _platform_lookup[sys.platform][LOOKUP_KEY][version_tuple[0]]
                # if type is dict, it is an older platform like Mojave, whichs name is decided in the
                # minor revision number
                if type(tmp) is dict:
                    self.data = _platform_lookup[sys.platform][LOOKUP_KEY][version_tuple[0]][version_tuple[1]]
                # if type is a string it is a newer platform whichs name is decided in the major revision number
                elif type(tmp) is str:
                    self.data = tmp
            except UnknownVersionStringError:
                self.data = f"Cannot collect OS name. Unexpected version string format '{platformversion}'."
            except KeyError:
                self.data = f"Cannot collect OS name for platform version '{platformversion}'"

    @staticmethod
    def _verify_version_string(platformversion) -> None:
        # Assume, that this code will never see older platforms, than 10.x.
        expected_version_format = re.compile(r'^\d{2,}(\.\d{1,})?(\.\d{1,})?$')
        if not expected_version_format.match(platformversion):
            raise UnknownVersionStringError(f"Unexpected version string '{platformversion}'.")


class OSVersion(MacArtefact):
    """
    Tries to retrieve the OS version number.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        if sys.platform == 'darwin':
            self.data = platform.mac_ver()[VERSION_NUMBER_INDEX]


class OSTimezone(ArtefactBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        self.data = datetime.now().astimezone().tzname()


class SudoVersion(MacArtefact):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._supportedsystem = ('Darwin', 'Linux')

    def _collect(self) -> None:
        self.data = run_terminal_command(['sudo', '-V'])


class OSPlatform(ArtefactBase):
    """Collects the platform on which this script is running on."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        self.data = platform.system()
