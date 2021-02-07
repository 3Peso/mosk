from getpass import getuser

from baseclasses.artefact import ArtefactBase


class CurrentUser(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'Current User'
        self._collectionmethod = 'getpass.getuser'
        self._description = 'Collects the current user with the Python module getpass.'

    def collect(self):
        self._collecteddata = getuser()

    def gettitle(self):
        return self._title

    def getcollectionmethod(self):
        return self._collectionmethod

    def getdescription(self):
        return self._description
