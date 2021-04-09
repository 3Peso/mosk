import logging
import sys
import datetime

import pytsk3
import pyewf

from baseclasses.source import SourceBase
from businesslogic.support import str_to_bool


class FolderItemInfo:
    def __init__(self, name: bytes, itemtype, size, create, modify_date):
        self.Name = name
        self.Type = itemtype
        self.Size = size
        self._create = create
        self._modify_date = modify_date

    @property
    def create(self):
        timestamp = datetime.datetime.fromtimestamp(self._create)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def modify_date(self):
        timestamp = datetime.datetime.fromtimestamp(self._modify_date)
        return timestamp.strftime('%Y-%m-%d %H:%M:%S')


class FolderInfo:
    def __init__(self, folderpath, folderitems, imagefile):
        self._imagefile = imagefile
        self._folderitems = folderitems
        self._folderpath = folderpath

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, FolderInfo):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        result = f"Foler Path: '{self._imagefile}:{self._folderpath}'\r\n\r\n"
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


class EWFImageInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(EWFImageInfo, self).__init__(url="",
                                           type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()


class EWFImage(SourceBase):
    FILE_SYSTEM_OFFSETS = {
        "Fat32": 1048576
    }

    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        SourceBase.__init__(self, *args, **kwargs)
        self._imagefilepath = self.get_parameter('filepath')
        self._imagetype = self.get_parameter('imagetype')
        self._imageinfo = self._get_image_information()
        self._filesystem = self._attach_filesystem()
        self._filesysteminfo = {}

        if str_to_bool(self.get_parameter('discover')):
            self._built_filesystem_information()

    def _get_image_information(self):
        if self._imagetype == "ewf":
            try:
                filenames = pyewf.glob(self._imagefilepath)
            except IOError as ioerror:
                _, e, _ = sys.exc_info()
                self._logger.error(f"Invalid EWF format:\n{e}")
                raise ioerror

            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)
            img_info = EWFImageInfo(ewf_handle)
        else:
            img_info = pytsk3.Img_Info(self._imagefilepath)

        return img_info

    def _attach_filesystem(self):
        fs = None

        for fs_type in self.FILE_SYSTEM_OFFSETS.keys():
            try:
                fs = pytsk3.FS_Info(self._imageinfo, self.FILE_SYSTEM_OFFSETS[fs_type])
                break
            except IOError:
                _, e, _ = sys.exc_info()
                self._logger.info(f"Unable to open FS:\n{e}")
                fs = None

        if fs is None:
            self._logger.error("Could not attach image. Unkown filesystem.")

        return fs

    def _discover_folder(self, folder):
        root_dir = self._filesystem.open_dir(path=folder)

        self._logger.debug(f"'{folder}' loading info from image ...")
        for f in root_dir:
            name = f.info.name.name
            if f.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                f_type = "DIR"
            else:
                f_type = "FILE"
            size = f.info.meta.size
            create = f.info.meta.crtime
            modify = f.info.meta.mtime

            yield FolderItemInfo(name=name, itemtype=f_type, size=size, create=create, modify_date=modify)

    # TODO Could potentially be speed up by using a set instead of a list for the folder info objects
    def _built_filesystem_information(self, folderpath='/'):
        folderinfo = self.get_folder_information(folderpath)
        self._filesysteminfo[folderpath] = folderinfo

        for item in folderinfo:
            if item.Type == "DIR" and item.Name != b'.' and item.Name != b'..':
                self._built_filesystem_information(f"{folderpath}{item.Name.decode()}/")

    def get_folder_information(self, folderpath):
        if folderpath not in self._filesysteminfo.keys():
            folderinfo = FolderInfo(folderpath=folderpath, folderitems=set(self._discover_folder(folderpath)),
                                    imagefile=self._imagefilepath)
            self._filesysteminfo[folderpath] = folderinfo
            return folderinfo
        else:
            return self._filesysteminfo[folderpath]
