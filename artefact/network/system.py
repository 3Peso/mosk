from businesslogic.support import get_time, DEFAULT_TIME_SERVER
from baseclasses.artefact import ArtefactBase


class TimeFromNTPServer(ArtefactBase):
    TIMER_SERVER_ATTRIBUTE = 'ntpserver'

    __timeServer = DEFAULT_TIME_SERVER

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'TimeFromNTPServer'
        self._collectionmethod = 'Network call using socket connect.'
        self._description = 'Retrieves the time from a time server. Can be used as reference time.\r\n' \
                             'Requires network connection.'

    def __str__(self):
        result = "Time server: '{}' Collected Time: {}".format(self.__timeServer, self.data.collecteddata)
        result = self.data.get_metadata_as_str(result)
        return result

    def collect(self):
        self.__timeServer = self.get_parameter(self.TIMER_SERVER_ATTRIBUTE)
        time = get_time(ntpserver=self.__timeServer)
        self.data = time
