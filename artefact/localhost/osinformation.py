# TODO Refactor
# OS Timezone
import platform
import sys
from datetime import datetime

from baseclasses.artefact import ArtefactBase


METHOD_KEY = 'CollectionMethod'
DESCRIPTION_KEY = 'Description'
LOOKUP_KEY = 'lookup'
VERSION_NUMBER_INDEX = 0

_platform_lookup = {
    'darwin': {
        LOOKUP_KEY: {
            '10.10': 'Yosemite',
            '10.11': 'El Capitan',
            '10.12': 'Sierra',
            '10.13': 'High Sierra',
            '10.14': 'Mojave',
            '10.15': 'Catalina',
            '11.0': 'BigSur',
            '11.1': 'BigSur',
            '11.2': 'BigSur'
        },
        METHOD_KEY: 'platform.mac_ver()',
        DESCRIPTION_KEY: 'Collects MacOS version number with platform module and uses this '
                         'combined with an internal lookup table of the collector artefact '
                         'to determine the MacOS marekting name.'
    }
}


class OSName(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        documentation = self._collect_documentation()
        self._collectionmethod = documentation[METHOD_KEY]
        self._description = documentation[DESCRIPTION_KEY]
        self._title = 'OS Name'

    def collect(self):
        if sys.platform == 'darwin':
            self._collecteddata = \
                _platform_lookup[sys.platform][LOOKUP_KEY][platform.mac_ver()[VERSION_NUMBER_INDEX]]

    def gettitle(self) -> str:
        return self._title

    def getcollectionmethod(self) -> str:
        return self._collectionmethod

    def getdescription(self) -> str:
        return self._description

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


class OSVersion(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        documentation = self._collect_documentation()
        self._collectionmethod = documentation[METHOD_KEY]
        self._description = documentation[DESCRIPTION_KEY]
        self._title = 'OS Version'

    def collect(self):
        if sys.platform == 'darwin':
            self._collecteddata = platform.mac_ver()[VERSION_NUMBER_INDEX]

    def gettitle(self) -> str:
        return self._title

    def getcollectionmethod(self) -> str:
        return self._collectionmethod

    def getdescription(self) -> str:
        return self._description

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
        self._collecteddata = datetime.now().astimezone().tzname()

    def gettitle(self) -> str:
        return self._title

    def getcollectionmethod(self) -> str:
        return self._collectionmethod

    def getdescription(self) -> str:
        return self._description
