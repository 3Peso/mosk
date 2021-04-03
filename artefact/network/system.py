"""
mosk network module for classes collecting system information through a network.
"""

__author__ = '3Peso'
__all__ = ['TimeFromNTPServer']

import collections
import logging

from businesslogic.support import get_time, DEFAULT_TIME_SERVER
from baseclasses.artefact import ArtefactBase


NTPTime = collections.namedtuple('NTPTime', 'Time NTPServer')


class TimeFromNTPServer(ArtefactBase):
    """
    Retrieves the current time from a provided NTP server.
    """
    __timeServer = DEFAULT_TIME_SERVER
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._title = 'TimeFromNTPServer'
        self._collectionmethod = 'Network call using socket connect.'
        self._description = 'Retrieves the time from a time server. Can be used as reference time.\r\n' \
                            'Requires network connection.'

    def _collect(self):
        try:
            self.__timeServer = self.timeserver
        except AttributeError:
            self._logger.info(f"No time server provided. Using default: {DEFAULT_TIME_SERVER}")
        time = NTPTime(Time=get_time(ntpserver=self.__timeServer), NTPServer=self.__timeServer)
        self.data = time
