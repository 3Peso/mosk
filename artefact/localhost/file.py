"""
mosk localhost module for classes collecting file information.
"""

__author__ = '3Peso'
__all__ = ['FileExistence', 'FileContent', 'ShellHistoryOfAllUsers']

import logging
from collections import namedtuple
from os import path

from baseclasses.artefact import ArtefactBase, MacArtefact
from source.localhost import expandfilepath
from businesslogic.support import get_userfolders

TermianlHistory = namedtuple('TerminalHistory', ['Path', 'Content'])


class FileExistence(ArtefactBase):
    """
    Tests if a file exsists under the provided path and returns True or False accordingly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        filepath = expandfilepath(self.filepath)
        if path.exists(filepath):
            self.data = f"File '{filepath}' exists."
            self.data[-1].sourcepath = filepath
        else:
            self.data = f"File '{filepath}' does not exist."


class FileContent(ArtefactBase):
    """
    Retrieves the file content of a file provided by path. It does NOT copy the file itself. The
    content is stored inside the log created during the collection session.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        filepath = expandfilepath(self.filepath)
        if path.exists(filepath):
            with open(filepath, "r") as filetoload:
                self.data = filetoload.read()
            self.data[-1].sourcepath = filepath
        else:
            self.data = f"File '{self.filepath}' does not exist."


class ShellHistoryOfAllUsers(MacArtefact):
    """
    Tries to access all user folders of a macOS installation and then it iterates over the possible shell history
    files (.bash_history and .zhs_history).
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        userfolders = set(get_userfolders())
        for history in ShellHistoryOfAllUsers._collect_bash_history(userfolders):
            self.data = history.Content
            self.data[-1].sourcepath = history.Path

    @staticmethod
    def _collect_bash_history(userfolders):
        historyfilepaths = (path.join(folder, history) for folder in userfolders
                            for history in ['.bash_history', '.zsh_history'])
        for historyfile in historyfilepaths:
            if path.exists(historyfile):
                ShellHistoryOfAllUsers._logger.debug("Found terminal history file '{}'.".format(historyfile))
                with open(historyfile, encoding='unicode_escape') as hf:
                    yield TermianlHistory(Path=historyfile, Content=hf.read())


class FileCopy(MacArtefact):
    """
    Tries to copy the file provided by 'filepath', and optionally, tries to collect the metadata of the file
    also, stored in a seperated file acompanying the file copy itself.
    The file copy is stored alongside the collection log. The collection log points to the copied file, but
    does not hold it.
    """
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def _collect(self):
        pass