"""
mosk mac module for classes collecting file information.
"""

__version__ = '0.0.6'
__author__ = '3Peso'
__all__ = ['ShellHistoryOfAllUsers']

import logging
from collections import namedtuple
from os import path

from baseclasses.artefact import ArtefactBase
from businesslogic.support import get_userfolders


TermianlHistory = namedtuple('TerminalHistory', ['Path', 'Content'])


class ShellHistoryOfAllUsers(ArtefactBase):
    """
    Tries to access all user folders of a macOS installation and then it iterates over the possible shell history
    files (.bash_history and .zhs_history).
    """
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._supportedsystem = 'darwin'

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
