"""
mosk localhost module for classes collecting infromation about the current user.
"""

__version__ = '0.0.2'
__author__ = '3Peso'
__all__ = ['CurrentUser', 'AllUsernames']

import logging
from pwd import getpwall
from getpass import getuser

from baseclasses.artefact import ArtefactBase
from businesslogic.support import str_to_bool, get_userfolders


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


class AllUsernames(ArtefactBase):
    """
    Gets all user names retrievable by python.
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'AllUsernames'
        self._collectionmethod = 'pwd.getpwall'
        self._description = 'Collects all usernames with the Python module pwd.'
        # Which properties of 'pwd.getpwall' will be controlled by the 'properties' parameter of the
        # collector, which is a string of property names seperated by comma.
        self.__properties = (item for item in self.properties.split(','))
        try:
            self.__users_with_homedir = str_to_bool(self.users_with_homedir)
            self._logger.debug('Collecting users with home directory: {}'.format(self.__users_with_homedir))
        except KeyError:
            self.__users_with_homedir = False

    def collect(self):
        for pw in getpwall():
            if not self.__users_with_homedir:
                self.data = ["{}: {}".format(prop, getattr(pw, prop)) for prop in self.__properties]
            else:
                homedirs = (user.name for user in get_userfolders())
                username = getattr(pw, 'pw_name')
                if username in homedirs:
                    self._logger.debug('"{} user collected"'.format(username))
                    self.data = ["{}: {}".format(prop, getattr(pw, prop)) for prop in self.__properties]
