"""
mosk network module for classes collecting system information through a network.
"""

__author__ = '3Peso'
__all__ = ['TimeFromNTPServer']

import collections
import logging
import socket
from logging import Logger

from businesslogic.support import get_time, DEFAULT_TIME_SERVER
from baseclasses.artefact import ArtefactBase


NTPTime = collections.namedtuple('NTPTime', 'Time NTPServer')


class TimeFromNTPServer(ArtefactBase):
    """
    Retrieves the current time from a provided NTP server.
    """
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        try:
            self.__timeServer = self.timeserver
        except AttributeError:
            self._logger.info(f"No time server provided. Using default: {DEFAULT_TIME_SERVER}")
            self.timeserver = DEFAULT_TIME_SERVER
            self.__timeServer = DEFAULT_TIME_SERVER

        try:
            time = NTPTime(Time=get_time(ntpserver=self.__timeServer), NTPServer=self.__timeServer)
            self.data = time.Time
        except socket.gaierror as sock_err:
            self._logger.error(f"Could not retrieve network time. socket.gaierror: {sock_err.args[1]}")
            self.data = f"Could not retrieve network time because of a runtime exception. " \
                        f"socket.gaierror message: {sock_err.args[1]}"

    def _cleanup(self):
        pass
