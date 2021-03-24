"""
mosk localhost module for classes collecting os information.
"""

__version__ = '0.0.4'
__author__ = '3Peso'
__all__ = ['OSName', 'OSVersion', 'OSTimezone']

import platform
import sys
import subprocess
from datetime import datetime

from baseclasses.artefact import ArtefactBase


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
        },
        METHOD_KEY: 'platform.mac_ver()',
        DESCRIPTION_KEY: 'Collects MacOS version number with platform module and uses this \r\n'
                         'combined with an internal lookup table of the collector artefact \r\n'
                         'to determine the MacOS marekting name.'
    }
}


class OSName(ArtefactBase):
    """
    Tries to look up the installed OS name.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        documentation = self._collect_documentation()
        self._collectionmethod = documentation[METHOD_KEY]
        self._description = documentation[DESCRIPTION_KEY]
        self._title = 'OS Name'

    def collect(self):
        if sys.platform == 'darwin':
            platformversion = platform.mac_ver()[VERSION_NUMBER_INDEX]
            try:
                self.data = _platform_lookup[sys.platform][LOOKUP_KEY][platformversion]
            except KeyError:
                self.data = "Cannot collect OS name for platform version '{}'".format(platformversion)

    @classmethod
    def _collect_documentation(cls):
        documentation = {}
        if sys.platform not in _platform_lookup.keys():
            documentation[METHOD_KEY] = "Platform '{}' is currently not supported.".format(sys.platform)
            documentation[DESCRIPTION_KEY] = "Platform '{}' is currently not supported.".format(sys.platform)
        else:
            documentation[METHOD_KEY] = _platform_lookup[sys.platform][METHOD_KEY]
            documentation[DESCRIPTION_KEY] = _platform_lookup[sys.platform][DESCRIPTION_KEY]

        return documentation


class OSVersion(ArtefactBase):
    """
    Tries to retrieve the OS version number.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        documentation = self._collect_documentation()
        self._collectionmethod = documentation[METHOD_KEY]
        self._description = documentation[DESCRIPTION_KEY]
        self._title = 'OS Version'

    def collect(self):
        if sys.platform == 'darwin':
            self.data = platform.mac_ver()[VERSION_NUMBER_INDEX]

    @staticmethod
    def _collect_documentation():
        documentation = {}
        if sys.platform not in _platform_lookup.keys():
            documentation[METHOD_KEY] = "Platform '{}' is currently not supported.".format(sys.platform)
            documentation[DESCRIPTION_KEY] = "Platform '{}' is currently not supported.".format(sys.platform)
        else:
            documentation[METHOD_KEY] = _platform_lookup[sys.platform][METHOD_KEY]
            documentation[DESCRIPTION_KEY] = _platform_lookup[sys.platform][DESCRIPTION_KEY]

        return documentation


class OSTimezone(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'OS Timezone'
        self._collectionmethod = 'datetime.now astimezone'
        self._description = 'Collect the local timezone by using the Python module datetime.'

    def collect(self):
        self.data = datetime.now().astimezone().tzname()


class SudoVersion(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'Sudo Version Collector'
        self._collectionmethod = 'sudo -V in Shell'
        self._description = \
            "Collects all information about the current SUDO version. According to CVE-2021-3156\r\n" \
            "the versions 1.7.7 through 1.7.10p9, 1.8.2 through 1.8.31p2, and 1.9.0 through 1.9.5p1\r\n" \
            "are vulnurable to get root level access if you have access to the machine."

    def collect(self):
        process = subprocess.Popen(['sudo', '-V'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        self.data = process.communicate()[0]
