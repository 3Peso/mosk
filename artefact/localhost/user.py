"""
mosk localhost module for classes collecting infromation about the current user.
"""

__author__ = '3Peso'

import logging
import platform
import subprocess
from logging import Logger
from os import path
if platform.system() != "Windows":
    from pwd import getpwall
from getpass import getuser

from baseclasses.artefact import ArtefactBase, MacArtefact, LinuxArtefact, ToolClass
from businesslogic.support import str_to_bool, get_userfolders, validate_file_signature
from businesslogic.errors import SignatureMatchError


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


class RecentUserItems(MacArtefact, ToolClass):
    """
    Collects the recent items the current user has opened from the home directory of the user.
    """

    def __init__(self, *args, **kwargs):
        #self._mdfind_path = ""
        self._tool_path = ""
        self._default_tool = "mdfind"
        super().__init__(*args, **kwargs)

    def _collect(self):
        proc = subprocess.Popen([f"{self.tool_path} -onlyin $HOME "
                                 f"'((kMDItemContentModificationDate > $time.now(-60m)) "
                                 f"&& (kMDItemContentModificationDate < $time.now()))'"],
                                stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        self.data = out.decode("utf-8")

#    @property
#    def mdfind_path(self):
#        logger = logging.getLogger(__name__)
#        if self._mdfind_path == "":
#            logger.warning("mdfind path not set. Using 'mdfind' of live system.")
#            return "mdfind"
#        return self._mdfind_path

#    @mdfind_path.setter
#    def mdfind_path(self, value):
#        if path.exists(value):
#            if validate_file_signature(value):
#                self._mdfind_path = value
#            else:
#                raise SignatureMatchError(f"Signature for '{value}' does not match with expected signature.")


class UserStartUpPrograms(MacArtefact):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        # Launched BEFORE login
        # Collect LaunchAgents.plists from /System/Library/LaunchAgents
        # Collect LaunchDeamons.plists from /System/Library/LaunchDeamnons

        # Launched AFTER login
        # Collect LaunchAgents.plists from ~/Library/LaunchAgents
        #    RunAtLoad key must be set to True
        #    ProgramAttributes (also interessting)
        # Until 10.12 collect entries from ~/Library/Preferences/com.apple.loginitems.plist
        # Starting with 10.13 collect entries from ~/Library/Application Support/com.apple.backgroundtaskmanagementagent/backgrounditems.btm
        # Collect all currently running apps (which can be relaunched after a reboot)
        pass