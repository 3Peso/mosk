from os import path

from baseclasses.artefact import ArtefactBase
from source.localhost import expandfilepath


class FileExistence(ArtefactBase):
    """
    Tests if a file exsists under the provided path and returns True or False accordingly.
    """
    FILE_PATH_PARAMETER = "filepath"

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'Filesystem'
        self._collectionmethod = 'os.path.exists'
        self._description = 'Find a file by file name including the path or parts of the path.'

    def collect(self):
        filepath = self._parameters[self.FILE_PATH_PARAMETER]
        filepath = expandfilepath(filepath)
        if path.exists(filepath):
            self.data = "File '{}' exists.".format(filepath)
            self.data.sourcepath = filepath
        else:
            self.data = "File '{}' does not exist.".format(filepath)


class FileContent(ArtefactBase):
    """
    Retrieves the file content of a file provided by path.
    """
    FILE_PATH_PARAMETER = "filepath"

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = "File content collector"
        self._collectionmethod = "python file context manager"
        self._description = "Uses the python file context manager to open the file in read mode and store its\r\n" \
                            "content and a MD5 hash of its content."

    def collect(self):
        filepath = self._parameters[self.FILE_PATH_PARAMETER]
        filepath = expandfilepath(filepath)
        if path.exists(filepath):
            with open(filepath, "r") as filetoload:
                self.data = filetoload.read()
            self.data.sourcepath = filepath
        else:
            self.data = "File '{}' does not exist.".format(
                self.get_parameter(self.FILE_PATH_PARAMETER))
