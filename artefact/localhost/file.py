"""
mosk localhost module for classes collecting file information.
"""

__version__ = '0.0.6'
__author__ = '3Peso'
__all__ = ['FileExistence', 'FileContent']

from os import path

from baseclasses.artefact import ArtefactBase
from source.localhost import expandfilepath


class FileExistence(ArtefactBase):
    """
    Tests if a file exsists under the provided path and returns True or False accordingly.
    """

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)

    def collect(self):
        filepath = expandfilepath(self.filepath)
        if path.exists(filepath):
            self.data = "File '{}' exists.".format(filepath)
            self.data[-1].sourcepath = filepath
        else:
            self.data = "File '{}' does not exist.".format(filepath)


class FileContent(ArtefactBase):
    """
    Retrieves the file content of a file provided by path.
    """
    FILE_PATH_PARAMETER = "filepath"

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)

    def collect(self):
        filepath = expandfilepath(self.filepath)
        if path.exists(filepath):
            with open(filepath, "r") as filetoload:
                self.data = filetoload.read()
            self.data[-1].sourcepath = filepath
        else:
            self.data = "File '{}' does not exist.".format(self.filepath)
