from pwd import getpwall

from baseclasses.artefact import ArtefactBase


class AllUsernames(ArtefactBase):
    _title = 'AllUsernames'
    _collectionmethod = 'pwd.getpwall'
    _description = 'Collects all usernames with the Python module pwd.'

    def collect(self):
        self._collecteddata = getpwall()

    def gettitle(self) -> str:
        return self._title

    def getcollectionmethod(self) -> str:
        return self._collectionmethod

    def getdescription(self) -> str:
        return self._description
