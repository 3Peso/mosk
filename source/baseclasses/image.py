__author__ = '3Peso'
__all__ = ['Image', 'FolderInfo', 'FolderItemInfo']

import logging
import datetime
import os
from logging import Logger
from collections import namedtuple
from abc import abstractmethod

from baseclasses.source import SourceBase
from businesslogic.support import format_bytes
from businesslogic.errors import ImageFileError

ImageType = namedtuple('ImageType', ['Type', 'FileEnding'])


class FolderItemInfo:
    def __init__(self, name: bytes, itemtype: str, size: int, create: int, modify_date: int, offset: int):
        self.Name: bytes = name
        self.Type: str = itemtype
        self.Size: int = size
        self._create: int = create
        self._modify_date: int = modify_date
        self.Offset: int = offset

    @property
    def create(self) -> datetime.datetime:
        timestamp: datetime.datetime = datetime.datetime.fromtimestamp(self._create)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def modify_date(self) -> datetime.datetime:
        timestamp: datetime.datetime = datetime.datetime.fromtimestamp(self._modify_date)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')


class FolderInfo:
    def __init__(self, folderpath: str, folderitems: set, imagefile: str, partitionindex: int):
        self._imagefile: str = imagefile
        self._folderitems: set = folderitems
        self._folderpath: str = folderpath
        self._partitionindex: int = partitionindex

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, FolderInfo):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self) -> str:
        result: str = f"Foler Path: '{self._imagefile}:{self._folderpath}'\r\n"
        result += f"Partition Index: '{self._partitionindex}\r\n\r\n"
        headers: list = ['Name', 'Type', 'Size', 'Create Date', 'Modify Date']
        row_format: str = "{:<45}{:<10}{:<10}{:<21}{:<21}\r\n"
        result += row_format.format(*headers) + "\r\n"
        for item in self._folderitems:
            result += row_format.format(item.Name.decode(), item.Type, str(format_bytes(item.Size)),
                                        str(item.create), str(item.modify_date))

        return result

    def __iter__(self):
        for item in self._folderitems:
            yield item

    @staticmethod
    def get_cvs_header() -> str:
        return "PartitionIndex,Path,Type,Size,CreateDate,ModifyDate"

    def get_folder_items_in_csv_format(self) -> str:
        """
        For every item in the folder yields a comma seperated string.
        """
        for item in self._folderitems:

            folderpath: str = self._folderpath.strip('/')
            filepath: str = ""
            if folderpath != "":
                filepath = "/".join([self._imagefile, str(self._partitionindex), folderpath,
                                     item.Name.decode()])
            else:
                filepath = f"{self._imagefile}/{str(self._partitionindex)}/{item.Name.decode()}"
            result: str = ",".join([str(self._partitionindex), filepath, item.Type, str(format_bytes(item.Size)),
                               str(item.create), str(item.modify_date)])
            yield result


class Image(SourceBase):
    IMAGE_TYPE_EWF: ImageType = ImageType(Type='ewf', FileEnding='.e01')
    DEFAULT_FS_TYPE: str = 'MAC'

    def __init__(self, *args, **kwargs):
        logger: Logger = logging.getLogger(__name__)
        super().__init__(*args, **kwargs)
        self._imagetype: ImageType = None
        self.imagefilepath: str = self.get_parameter('filepath')
        try:
            self._fstype = self.get_parameter('fstype')
        except KeyError:
            logger.warning("No image type parameter 'fstype' provided. Defaulting to 'MAC'.")
            self._fstype = self.DEFAULT_FS_TYPE

    @property
    def imagefilepath(self) -> str:
        return self._imagefilepath

    @imagefilepath.setter
    def imagefilepath(self, value: str) -> None:
        if not value.lower().endswith(self.IMAGE_TYPE_EWF.FileEnding):
            raise ImageFileError(f"Currently only {self.IMAGE_TYPE_EWF.Type} files"
                             f" (file ending '{self.IMAGE_TYPE_EWF.FileEnding}' are supported.")
        if not os.path.exists(value):
            raise FileNotFoundError(f"Image file '{value}' not found.")

        self._imagetype: ImageType = self.IMAGE_TYPE_EWF
        self._imagefilepath: str = value

    @abstractmethod
    def get_folder_information(self, folderpath: str, partitionindex: int) -> FolderInfo:
        pass

    @abstractmethod
    def get_partition_table(self):
        pass

    @abstractmethod
    def get_image_metadata(self):
        pass

    @abstractmethod
    def export_file(self, partitionindex: int, filepath: str, outpath: str) -> None:
        pass
