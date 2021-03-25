"""
mosk localhost module for classes collecting information about all users.
"""

__version__ = '0.0.5'
__author__ = '3Peso'
__all__ = ['AllUsernames']

import logging
from pwd import getpwall

from baseclasses.artefact import ArtefactBase
from businesslogic.support import str_to_bool, get_userfolders


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
        # inside the parameters variable
        self.__properties = [item for item in kwargs['parameters']['properties'].split(',')]
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
