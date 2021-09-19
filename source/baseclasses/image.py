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

ImageType = namedtuple('ImageType', ['Type', 'FileEnding'])


class Image(SourceBase):
    IMAGE_TYPE_EWF: ImageType = ImageType(Type='ewf', FileEnding='.e01')
    DEFAULT_FS_TYPE: str = 'MAC'

    def __init__(self, *args, **kwargs):
        logger: Logger = logging.getLogger(__name__)
        super().__init__(*args, **kwargs)
        self._imagetype: ImageType = None
        self.imagefilepath = self.get_parameter('filepath')
        try:
            self._fstype = self.get_parameter('fstype')
        except KeyError:
            logger.warning("No image type parameter 'fstype' provided. Defaulting to 'MAC'.")
            self._fstype = self.DEFAULT_FS_TYPE

    @property
    def imagefilepath(self):
        return self._imagefilepath

    @imagefilepath.setter
    def imagefilepath(self, value: str):
        if value.lower().endswith(self.IMAGE_TYPE_EWF.FileEnding):
            self._imagetype = self.IMAGE_TYPE_EWF
            if os.path.exists(value):
                self._imagefilepath = value
            else:
                raise FileNotFoundError(f"Image file '{value}' not found.")
        else:
            raise ValueError(f"Currently only {self.IMAGE_TYPE_EWF.Type} files"
                             f" (file ending '{self.IMAGE_TYPE_EWF.FileEnding}' are supported.")

    @abstractmethod
    def get_folder_information(self, folderpath, partitionindex):
        pass

    @abstractmethod
    def get_partition_table(self):
        pass

    @abstractmethod
    def get_image_metadata(self):
        pass

    @abstractmethod
    def export_file(self, partitionindex, filepath, outpath):
        pass


class FolderItemInfo:
    def __init__(self, name: bytes, itemtype, size, create, modify_date, offset):
        self.Name = name
        self.Type = itemtype
        self.Size = size
        self._create = create
        self._modify_date = modify_date
        self.Offset = offset

    @property
    def create(self):
        timestamp = datetime.datetime.fromtimestamp(self._create)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def modify_date(self):
        timestamp = datetime.datetime.fromtimestamp(self._modify_date)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')


class FolderInfo:
    def __init__(self, folderpath, folderitems, imagefile, partitionindex):
        self._imagefile = imagefile
        self._folderitems = folderitems
        self._folderpath = folderpath
        self._partitionindex = partitionindex

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, FolderInfo):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        result = f"Foler Path: '{self._imagefile}:{self._folderpath}'\r\n"
        result += f"Partition Index: '{self._partitionindex}\r\n\r\n"
        headers = ['Name', 'Type', 'Size', 'Create Date', 'Modify Date']
        row_format = "{:<45}{:<10}{:<10}{:<21}{:<21}\r\n"
        result += row_format.format(*headers) + "\r\n"
        for item in self._folderitems:
            result += row_format.format(item.Name.decode(), item.Type, str(format_bytes(item.Size)),
                                        str(item.create), str(item.modify_date))

        return result

    def __iter__(self):
        for item in self._folderitems:
            yield item

    @staticmethod
    def get_cvs_header():
        return "PartitionIndex,Path,Type,Size,CreateDate,ModifyDate"

    def get_folder_items_in_csv_format(self):
        """
        For every item in the folder yields a comma seperated string.
        """
        for item in self._folderitems:

            folderpath = self._folderpath.strip('/')
            filepath = ""
            if folderpath != "":
                filepath = "/".join([self._imagefile, str(self._partitionindex), folderpath,
                                     item.Name.decode()])
            else:
                filepath = f"{self._imagefile}/{str(self._partitionindex)}/{item.Name.decode()}"
            result = ",".join([str(self._partitionindex), filepath, item.Type, str(format_bytes(item.Size)),
                               str(item.create), str(item.modify_date)])
            yield result
