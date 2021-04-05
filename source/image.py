import logging
import sys
from collections import namedtuple

import pytsk3
import pyewf

from baseclasses.source import SourceBase
from businesslogic.support import str_to_bool


FolderItem = namedtuple('FolderItem', ['Name', 'Type', 'Size', 'Create', 'Modify_Date'])


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
            self.built_filesystem_information()

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

            yield FolderItem(Name=name, Type=f_type, Size=size, Create=create, Modify_Date=modify)

    def get_folder_information(self, folder):
        if folder not in self._filesysteminfo.keys():
            folderinfo = set(self._discover_folder(folder))
            self._filesysteminfo[folder] = folderinfo
            return folderinfo
        else:
            return self._filesysteminfo[folder]

    # TODO sets would be more performat instead of a dictionary. Implement a hashable class to represent a folder
    # with its items and add this to a set.
    def built_filesystem_information(self, folderpath='/'):
        folderitems = self.get_folder_information(folderpath)
        self._filesysteminfo[folderpath] = folderitems

        for item in folderitems:
            if item.Type == "DIR" and item.Name != b'.' and item.Name != b'..':
                self.built_filesystem_information(f"{folderpath}{item.Name.decode()}/")
