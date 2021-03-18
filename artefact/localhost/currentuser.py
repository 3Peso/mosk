from getpass import getuser

from baseclasses.artefact import ArtefactBase


class CurrentUser(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'Current User'
        self.__collectionmethod = 'getpass.getuser'
        self.__description = 'Collects the current user with the Python module getpass.'

    def collect(self):
        self.data = getuser()

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description
