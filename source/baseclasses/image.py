import logging
import datetime
from abc import abstractmethod

from baseclasses.source import SourceBase


class Image(SourceBase):
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._imagefilepath = self.get_parameter('filepath')
        self._imagetype = self.get_parameter('imagetype')
        try:
            self._fstype = self.get_parameter('fstype')
        except KeyError:
            self._logger.warning("No image type parameter 'fstype' provided. Defaulting to 'MAC'.")
            self._fstype = 'MAC'

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
            result += row_format.format(item.Name.decode(), item.Type, str(item.Size),
                                        str(item.create), str(item.modify_date))

        return result

    def __iter__(self):
        for item in self._folderitems:
            yield item
