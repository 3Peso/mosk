"""
mosk localhost module for classes collecting infromation about the current user.
"""

__author__ = '3Peso'

import logging
from logging import Logger
from pwd import getpwall
from getpass import getuser

from baseclasses.artefact import ArtefactBase, MacArtefact, LinuxArtefact
from businesslogic.support import str_to_bool, get_userfolders


class CurrentUser(ArtefactBase):
    """
    Gets the name of the currently authenticated user running the script.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        self.data = getuser()


class AllUsernames(MacArtefact, LinuxArtefact):
    """
    Gets all user names retrievable by python.
    """
    _logger: Logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Which properties of 'pwd.getpwall' will be controlled by the 'properties' parameter of the
        # collector, which is a string of property names seperated by comma.
        self.__properties  = (item for item in self.properties.split(','))
        try:
            self.__users_with_homedir = str_to_bool(self.users_with_homedir)
            self._logger.debug(f'Collecting users with home directory: {self.__users_with_homedir}')
        except KeyError:
            self.__users_with_homedir = False

    def _collect(self) -> None:
        for pw in getpwall():
            if not self.__users_with_homedir:
                self.data = [f"{prop}: {getattr(pw, prop)}" for prop in self.__properties]
            else:
                homedirs = (user.name for user in get_userfolders())
                username = getattr(pw, 'pw_name')
                if username in homedirs:
                    self._logger.debug('f"{username} user collected"')
                    self.data = [f"{prop}: {getattr(pw, prop)}" for prop in self.__properties]
