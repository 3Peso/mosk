import socket

from baseclasses.artefact import ArtefactBase
from businesslogic.log import mosk_logger


class MachineName(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'Machine Name'
        self.__collectionmethod = 'socket.gethostname()'
        self.__description = 'Collects the machine name of the local host with the Python module socket'

    def collect(self):
        self._collecteddata = socket.gethostname()
        if self._collecteddata is not None:
            mosk_logger.debug("artefact.localhost.machineinformation: Machine name '{}' has been collected.".
                              format(self._collecteddata))
        else:
            mosk_logger.info("artefact.localhost.machineinformation: Could not colelct machine name.")

    def gettitle(self):
        return self.__title

    def getcollectionmethod(self):
        return self.__collectionmethod

    def getdescription(self):
        return self.__description
