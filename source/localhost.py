import logging

from baseclasses.source import SourceBase
from os import path
from pathlib import Path


__author__ = '3Peso'
__all__ = ['LocalHost']


class LocalHost(SourceBase):
    def __init__(self, *args, **kwargs):
        SourceBase.__init__(self, *args, **kwargs)


def expandfilepath(filepath: str):
    if '~' not in filepath:
        return filepath

    homepath: str = str(Path.home())
    filepath = filepath.split('~')[-1]
    if filepath.startswith('/'):
        filepath: str = filepath[1:]
    filepath = path.join(homepath, filepath)
    logger = logging.getLogger(__name__)
    logger.debug("Path '{}' expanded.".format(filepath))
    return filepath
