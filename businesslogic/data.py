import os
import hashlib

import businesslogic.support


class CollectionData:
    def __init__(self, data, currentdatetime=None):
        self.collecteddata = data
        self.currentdatetime = currentdatetime
        self._sourcehash = None
        self._sourcepath = None

    # TODO Rework metadata formatting
    def __str__(self):
        result = "{}".format(self.collecteddata)
        result = self.get_metadata_as_str(result)
        return result

    def get_metadata_as_str(self, prepend=''):
        if prepend != '':
            prepend = "{}\r\n".format(prepend)
        if self.currentdatetime is not None:
            prepend += "\r\nCollection Time Stamp: {}".format(self.currentdatetime)
        if self.sourcehash is not None:
            prepend += "\r\nSource MD5: {}".format(self.sourcehash)
        if self.sourcepath is not None:
            prepend += "\r\nSource path: {}".format(self.sourcepath)

        return prepend

    @property
    def sourcehash(self):
        return self._sourcehash

    def save_as_md5(self, value: str):
        self._sourcehash = hashlib.md5(value.encode('ascii')).hexdigest()

    @property
    def sourcepath(self):
        return self._sourcepath

    # TODO more robust validation required
    @sourcepath.setter
    def sourcepath(self, value):
        if value is not None and os.path.exists(value):
            self._sourcehash = businesslogic.support.md5(value)
            self._sourcepath = value
