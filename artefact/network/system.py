"""
mosk network module for classes collecting system information through a network.
"""

__version__ = '0.0.3'
__author__ = '3Peso'
__all__ = ['TimeFromNTPServer']

import collections

from businesslogic.support import get_time, DEFAULT_TIME_SERVER
from baseclasses.artefact import ArtefactBase


NTPTime = collections.namedtuple('NTPTime', 'Time NTPServer')


class TimeFromNTPServer(ArtefactBase):
    """
    Retrieves the current time from a provided NTP server.
    """
    TIMER_SERVER_ATTRIBUTE = 'ntpserver'

    __timeServer = DEFAULT_TIME_SERVER

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'TimeFromNTPServer'
        self._collectionmethod = 'Network call using socket connect.'
        self._description = 'Retrieves the time from a time server. Can be used as reference time.\r\n' \
                            'Requires network connection.'

    def collect(self):
        self.__timeServer = self.get_parameter(self.TIMER_SERVER_ATTRIBUTE)
        time = NTPTime(Time=get_time(ntpserver=self.__timeServer), NTPServer=self.__timeServer)
        self.data = time
