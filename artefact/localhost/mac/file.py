from os import path
from pathlib import Path

from baseclasses.artefact import ArtefactBase
from source.localhost import expandfilepath


class FileContent(ArtefactBase):
    FILE_PATH_PARAMETER = "filepath"

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)

    def collect(self):
        filepath = self._parameters[self.FILE_PATH_PARAMETER].nodeValue
        filepath = expandfilepath(filepath)
        if path.exists(filepath):
            with open(filepath) as filetoload:
                self._collecteddata = filetoload.read()
        else:
            self._collecteddata = "File '{}' does not exist.".format(
                self._parameters[self.FILE_PATH_PARAMETER].nodeValue)
