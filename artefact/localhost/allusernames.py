"""
mosk localhost module for classes collecting information about all users.
"""

__version__ = '0.0.3'
__author__ = '3Peso'
__all__ = ['AllUsernames']

from pwd import getpwall

from baseclasses.artefact import ArtefactBase


# TODO Implement switch to collect only users with a folder in '/users/*'
class AllUsernames(ArtefactBase):
    """
    Gets all user names retrievable by python.
    """
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'AllUsernames'
        self._collectionmethod = 'pwd.getpwall'
        self._description = 'Collects all usernames with the Python module pwd.'
        # inside the parameters variable
        self.__properties = [item for item in kwargs['parameters']['properties'].split(',')]

    def collect(self):
        for pw in getpwall():
            self.data = ["{}: {}".format(prop, getattr(pw, prop)) for prop in self.__properties]
