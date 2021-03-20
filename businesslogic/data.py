import os

import businesslogic.support

class CollectionData:
    def __init__(self, data, currentdatetime=None):
        self.collecteddata = data
        self.currentdatetime = currentdatetime
        self._sourcehash = None
        self._sourcepath = None

    # TODO Rework metadata formatting
    def __str__(self):
        result = "{}\r\n".format(self.collecteddata)
        if self.currentdatetime is not None:
            result += "\r\nCollection Time Stamp: {}".format(self.currentdatetime)
        if self.sourcehash is not None:
            result += "\r\nSource MD5: {}".format(self.sourcehash)
        if self.sourcepath is not None:
            result += "\r\nSource path: {}".format(self.sourcepath)

        return result

    @property
    def sourcehash(self):
        return self._sourcehash

    @property
    def sourcepath(self):
        return self._sourcepath

    # TODO more robust validation required
    @sourcepath.setter
    def sourcepath(self, value):
        if value is not None and os.path.exists(value):
            with open(value) as source:
                self._sourcehash = businesslogic.support.md5(value)
                self._sourcepath = value
