"""
Collection data module
"""

__author__ = '3Peso'
__all__ = ['CollectionData', 'CollectionMetaData']

import os
import hashlib
import json
from collections import OrderedDict

import businesslogic.support
from businesslogic.placeholders import Placeholder


class CollectionData:
    """
    CollectionData is the data container which stores the collected data in memory, and additionally required metadata
    as the path of the source file, if there is one,the colelction timestamp, and/or the MD5 hash of the collected data.
    """
    def __init__(self, data, currentdatetime=None, collector_name=None, collector_parameters=None):
        self.collecteddata = data
        self.currentdatetime = currentdatetime
        self._sourcehash = None
        self._sourcepath = None
        self._collector_name = collector_name
        self._collector_parameters = collector_parameters

    # TODO Rework metadata formatting
    def __str__(self):
        result = f'-- Collection Data     {"-" * 10}\r\n\r\n'
        result += f"{self.collecteddata}"
        result += f'\r\n\r\n-- Collection Metadata {"-" * 10}'
        result = self.get_metadata_as_str(result)
        result = self.get_collector_info_as_str(result)
        result += f'\r\n\r\n{"-" * 33}\r\n'
        return result

    def get_metadata_as_str(self, prepend=''):
        if prepend != '':
            prepend = f"{prepend}\r\n"
        if self.currentdatetime is not None:
            prepend += f"\r\nCollection Time Stamp: {self.currentdatetime}"
        if self.sourcehash is not None:
            prepend += f"\r\nSource MD5: {self.sourcehash}"
        if self.sourcepath is not None:
            prepend += f"\r\nSource path: {self.sourcepath}"

        return prepend

    def get_collector_info_as_str(self, prepend=''):
        if self._collector_name is None and self._collector_parameters is not None:
            raise ValueError('You must provide a collector name.')

        if self._collector_name is not None:
            prepend += f"\r\n\r\nCollector: {self._collector_name}"
        if self._collector_parameters is not None:
            for param in self._collector_parameters.keys():
                prepend += f"\r\n{param}: '{self._collector_parameters[param]}'"

        return prepend

    def get_json(self):
        j = {
            "CollectionTime": str(self.currentdatetime),
            "Data": str(self.collecteddata),
            "CollectorName": self._collector_name,
            "SourcePath": self._sourcepath,
            "SourceHash": self._sourcehash
        }

        for param, value in self._collector_parameters.items():
            j[param] = value

        return json.dumps(j)

    @property
    def sourcehash(self):
        return self._sourcehash

    # TODO refactor so that MD5 hash for longer strings can be added, too.
    def save_as_md5(self, value: str):
        # Only chunks of up to 4096 bytes can be crammed into an md5 hash. If they are longer
        # you have to split the strings.
        bvalue = value.encode('ascii')
        if len(bvalue) >= 4096:
            self._sourcehash = hashlib.md5(bvalue).hexdigest()
        else:
            raise ValueError("Provided value cannot be longer than 4096 bytes.")

    @property
    def sourcepath(self):
        return self._sourcepath

    # TODO more robust validation required
    @sourcepath.setter
    def sourcepath(self, value):
        if value is not None and os.path.exists(value):
            self._sourcehash = businesslogic.support.md5(value)
            self._sourcepath = value


class CollectionMetaData:
    """Will store the metadata regarding the whole collection process, like for example the task description."""
    def __init__(self, metadata: OrderedDict):
        self._collectionMetadata = metadata

    @property
    def metadata_fields(self):
        for field in self._collectionMetadata.keys():
            yield field

    @Placeholder
    def get_metadata(self, field):
        return self._collectionMetadata[field]
