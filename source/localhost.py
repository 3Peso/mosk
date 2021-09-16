import logging
from logging import Logger

from baseclasses.source import SourceBase
from os import path
from pathlib import Path

_logger: Logger = logging.getLogger(__name__)


class LocalHost(SourceBase):
    def __init__(self, *args, **kwargs):
        SourceBase.__init__(self, *args, **kwargs)


def expandfilepath(filepath: str):
    if '~' in filepath:
        homepath: str = str(Path.home())
        filepath = filepath.split('~')[-1]
        if filepath.startswith('/'):
            filepath: str = filepath[1:]
        filepath = path.join(homepath, filepath)
        _logger.debug("Path '{}' expanded.".format(filepath))
        return filepath
    else:
        return filepath
