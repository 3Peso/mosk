import socket

from baseclasses.artefact import ArtefactBase


class MachineName(ArtefactBase):
    _title = 'Machine Name'
    _collectionmethod = 'socket.gethostname()'
    _description = 'Collects the machine name of the local host with the Python module socket'

    def collect(self):
        self._collecteddata = socket.gethostname()

    def gettitle(self):
        return self._title

    def getcollectionmethod(self):
        return self._collectionmethod

    def getdescription(self):
        return self._description
