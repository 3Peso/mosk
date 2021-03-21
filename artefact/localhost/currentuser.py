from getpass import getuser

from baseclasses.artefact import ArtefactBase


class CurrentUser(ArtefactBase):
    """
    Gets the name of the currently authenticated user running the script.
    """
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'Current User'
        self._collectionmethod = 'getpass.getuser'
        self._description = 'Collects the current user with the Python module getpass.'

    def collect(self):
        self.data = getuser()
