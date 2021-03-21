import logging
import socket

from baseclasses.artefact import ArtefactBase


class MachineName(ArtefactBase):
    """
    Retrieves the name of the machine running this script.
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'Machine Name'
        self._collectionmethod = 'socket.gethostname()'
        self._description = 'Collects the machine name of the local host with the Python module socket'

    def collect(self):
        self.data = socket.gethostname()
        if self.data is not None:
            MachineName._logger.debug("Machine name '{}' has been collected.".
                                      format(self.data.collecteddata))
        else:
            MachineName._logger.info("Could not colelct machine name.")
