# TODO Refactor
# OS Timezone
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
            '10.10': 'Yosemite',
            '10.11': 'El Capitan',
            '10.12': 'Sierra',
            '10.13': 'High Sierra',
            '10.14': 'Mojave',
            '10.15': 'Catalina',
            '11.0': 'BigSur',
            '11.1': 'BigSur',
            '11.2': 'BigSur',
            '11.2.1': 'BigSur'
        },
        METHOD_KEY: 'platform.mac_ver()',
        DESCRIPTION_KEY: 'Collects MacOS version number with platform module and uses this \r\n'
                         'combined with an internal lookup table of the collector artefact \r\n'
                         'to determine the MacOS marekting name.'
    }
}


class OSName(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        documentation = self._collect_documentation()
        self.__collectionmethod = documentation[METHOD_KEY]
        self.__description = documentation[DESCRIPTION_KEY]
        self.__title = 'OS Name'

    def collect(self):
        if sys.platform == 'darwin':
            self._collecteddata = \
                _platform_lookup[sys.platform][LOOKUP_KEY][platform.mac_ver()[VERSION_NUMBER_INDEX]]

    def gettitle(self) -> str:
        return self.__title

    def getcollectionmethod(self) -> str:
        return self.__collectionmethod

    def getdescription(self) -> str:
        return self.__description

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        documentation = self._collect_documentation()
        self.__collectionmethod = documentation[METHOD_KEY]
        self.__description = documentation[DESCRIPTION_KEY]
        self.__title = 'OS Version'

    def collect(self):
        if sys.platform == 'darwin':
            self._collecteddata = platform.mac_ver()[VERSION_NUMBER_INDEX]

    def gettitle(self) -> str:
        return self.__title

    def getcollectionmethod(self) -> str:
        return self.__collectionmethod

    def getdescription(self) -> str:
        return self.__description

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
        self.__title = 'OS Timezone'
        self.__collectionmethod = 'datetime.now astimezone'
        self.__description = 'Collect the local timezone by using the Python module datetime.'

    def collect(self):
        self._collecteddata = datetime.now().astimezone().tzname()

    def gettitle(self) -> str:
        return self.__title

    def getcollectionmethod(self) -> str:
        return self.__collectionmethod

    def getdescription(self) -> str:
        return self.__description


class SudoVersion(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'Sudo Version Collector'
        self.__collectionmethod = 'sudo -V in Shell'
        self.__description = \
            "Collects all information about the current SUDO version. According to CVE-2021-3156\r\n" \
            "the versions 1.7.7 through 1.7.10p9, 1.8.2 through 1.8.31p2, and 1.9.0 through 1.9.5p1\r\n" \
            "are vulnurable to get root level access if you have access to the machine."

    def __str__(self):
        return self._collecteddata[0]

    def collect(self):
        process = subprocess.Popen(['sudo', '-V'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        self._collecteddata = process.communicate()

    def gettitle(self) -> str:
        return self.__title

    def getcollectionmethod(self) -> str:
        return self.__collectionmethod

    def getdescription(self) -> str:
        return self.__description
