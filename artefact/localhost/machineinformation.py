import socket

from baseclasses.artefact import ArtefactBase


class MachineName(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'Machine Name'
        self._collectionmethod = 'socket.gethostname()'
        self._description = 'Collects the machine name of the local host with the Python module socket'

    def collect(self):
        self._collecteddata = socket.gethostname()

    def gettitle(self):
        return self._title

    def getcollectionmethod(self):
        return self._collectionmethod

    def getdescription(self):
        return self._description
