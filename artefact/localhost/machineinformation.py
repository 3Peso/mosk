import logging
import socket

from baseclasses.artefact import ArtefactBase


class MachineName(ArtefactBase):
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'Machine Name'
        self.__collectionmethod = 'socket.gethostname()'
        self.__description = 'Collects the machine name of the local host with the Python module socket'

    def collect(self):
        self.data = socket.gethostname()
        if self.data is not None:
            MachineName._logger.debug("Machine name '{}' has been collected.".
                                      format(self.data.collecteddata))
        else:
            MachineName._logger.info("Could not colelct machine name.")

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description
