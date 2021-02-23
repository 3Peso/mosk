from os import path

from baseclasses.artefact import ArtefactBase


class FileExistence(ArtefactBase):
    FILE_PATH_PARAMETER = "filepath"

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'Filesystem'
        self.__collectionmethod = 'os.path.exists'
        self.__description = 'Find a file by file name including the path or parts of the path.'

    # TODO Currently the artefact stores XML attributes in its parameters. It should only store their value.
    def collect(self):
        if path.exists(self._parameters[self.FILE_PATH_PARAMETER].nodeValue):
            self._collecteddata = "File '{}' exists.".format(
                self._parameters[self.FILE_PATH_PARAMETER].nodeValue)
        else:
            self._collecteddata = "File '{}' does not exist.".format(
                self._parameters[self.FILE_PATH_PARAMETER].nodeValue)

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description
