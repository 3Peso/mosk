"""
Collection data module
"""

__author__ = '3Peso'
__all__ = ['CollectionData', 'CollectionMetaData']

import os
import json
from collections import OrderedDict

import businesslogic.support
from businesslogic.placeholders import Placeholder
from businesslogic.errors import NoCollectorError


class CollectionData:
    """
    CollectionData is the data container which stores the collected data in memory, and additionally required metadata
    as the path of the source file, if there is one,the colelction timestamp, and/or the MD5 hash of the collected data.
    """
    def __init__(self, data, currentdatetime = None, collector_name: str = None) -> None:
        if data != "":
            self.collecteddata = data
        else:
            self.collecteddata = "*No data collected*"
        self.currentdatetime = currentdatetime
        self._sourcehash = None
        self._sourcepath = None
        self._collector_name = collector_name
        self.collector_parameters = None

    def __str__(self) -> str:
        result = f'-- Collection Data     {"-" * 10}\r\n\r\n'
        result += f"{self._get_collection_data_as_str()}"
        result += f'\r\n\r\n-- Collection Metadata {"-" * 10}'
        result += f'\r\n{self.get_metadata_as_str()}'
        result += f'\r\n{self.get_collector_info_as_str()}'
        result += f'\r\n{"-" * 33}\r\n'
        return result.lstrip('\r\n')

    def _get_collection_data_as_str(self) -> str:
        if type(self.collecteddata) is not dict:
            return self.collecteddata
        else:
            data_as_string = ""
            for datafield in self.collecteddata:
                data_as_string += f"{datafield}: {self.collecteddata[datafield]}\n"
            return data_as_string.lstrip('\r\n').rstrip('\r\n')

    def get_metadata_as_str(self) -> str:
        """
        Returns all the collector metadata. This will be the timestamp the collector ran, and,
        if provided by the collector, the md5 hash of the data, the collector collected, and, if provided
        by the collector, the source file the collector used to collect the data.
        """
        metadata: str = ""
        if self.currentdatetime is not None:
            metadata += f"\r\nCollection Time Stamp: {self.currentdatetime}"
        if self.sourcehash is not None:
            metadata += f"\r\nSource MD5: {self.sourcehash}"
        if self.sourcepath is not None:
            metadata += f"\r\nSource path: {self.sourcepath}"

        return metadata.lstrip('\r\n').rstrip('\r\n')

    def get_collector_info_as_str(self) -> str:
        """
        Returns the collector name and the call parameters to run the collector in the first place
        as string.
        """
        if self._collector_name is None and self.collector_parameters is not None:
            raise NoCollectorError('You must provide a collector name.')

        info: str = ""
        if self._collector_name is not None:
            info += f"\r\n\r\nCollector: {self._collector_name}"
        if self.collector_parameters is not None:
            for param in self.collector_parameters.keys():
                # It happens, that a parameter value is not of the type string. In that case the conversion
                # helps. In every other case, type conversion will not hurt.
                info += f"\r\n{param}: '{str(self.collector_parameters[param]).strip()}'"

        return info.lstrip('\r\n').rstrip('\r\n')

    def get_json(self) -> str:
        """
        Returns the json representation of the ColletorData object.
        """
        j = {
            "CollectionTime": str(self.currentdatetime),
            "Data": str(self.collecteddata),
            "CollectorName": self._collector_name,
            "SourcePath": self._sourcepath,
            "SourceHash": self._sourcehash
        }

        for param, value in self.collector_parameters.items():
            j[param] = value

        return json.dumps(j)

    @property
    def sourcehash(self) -> str:
        return self._sourcehash

    @sourcehash.setter
    def sourcehash(self, value: str) -> None:
        self._sourcehash = value

    def save_as_md5(self, value: str):
        self._sourcehash = businesslogic.support.md5(data=value)

    @property
    def sourcepath(self) -> str:
        return self._sourcepath

    @sourcepath.setter
    def sourcepath(self, value: str) -> None:
        if value is not None and os.path.exists(value):
            self._sourcehash = businesslogic.support.md5(value)
            self._sourcepath = value
        else:
            raise FileNotFoundError(f"{value}")


class CollectionMetaData:
    """
    Will store the metadata regarding the whole collection process, like for example the task description.
    """
    def __init__(self, metadata: OrderedDict = None):
        self._collectionMetadata: OrderedDict = metadata

    @property
    def metadata_fields(self):
        for field in self._collectionMetadata.keys():
            yield field

    @Placeholder
    def get_metadata(self, field: str) -> str:
        return self._collectionMetadata[field]
