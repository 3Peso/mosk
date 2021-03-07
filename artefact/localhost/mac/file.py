import logging
import os
from collections import namedtuple
from os import path

from baseclasses.artefact import ArtefactBase
from source.localhost import expandfilepath


TermianlHistory = namedtuple('TerminalHistory', ['Path', 'Content'])


class BashHistoryOfAllUsers(ArtefactBase):
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)

    def __str__(self):
        result = ''
        for data in self._collecteddata:
            result = result + "{}START{}\nPATH: {}\n\nCONTENT:\n{}\n{} END {}".format('*' * 20, '*' * 20,
                                                                                      data.Path, data.Content,
                                                                                      '+' * 20, '+' * 20)
        return result

    def collect(self):
        userfolders = [f.path for f in os.scandir('/Users') if f.is_dir()]
        self._collecteddata = list(BashHistoryOfAllUsers._collect_bash_history(userfolders))

    @staticmethod
    def _collect_bash_history(userfolders):
        historyfilepaths = [path.join(folder, history) for folder in userfolders
                            for history in ['.bash_history', '.zsh_history']]
        for historyfile in historyfilepaths:
            if path.exists(historyfile):
                BashHistoryOfAllUsers._logger.debug("Found terminal history file '{}'.".format(historyfile))
                with open(historyfile, encoding='unicode_escape') as hf:
                    yield TermianlHistory(Path=historyfile, Content=hf.read())
