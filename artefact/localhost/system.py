from businesslogic.support import get_time, DEFAULT_TIME_SERVER
from baseclasses.artefact import ArtefactBase


class TimeFromNTPServer(ArtefactBase):
    __timeServer = DEFAULT_TIME_SERVER

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'TimeFromNTPServer'
        self.__collectionmethod = 'Network call using socket connect.'
        self.__description = 'Retrieves the time from a time server. Can be used as reference time.\r\n' \
                             'Requires network connection.'

    def __str__(self):
        return "Time server: '{}' Collected Time: {}".format(self.__timeServer, self._collecteddata)

    def collect(self):
        # TODO Provide time server by intructions
        time = get_time(ntpserver=self.__timeServer)
        self._collecteddata = time

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description
