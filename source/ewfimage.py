import logging
import sys
import pytsk3
import pyewf

from source.baseclasses.image import Image, FolderInfo, FolderItemInfo
from businesslogic.support import str_to_bool


class EWFImage(Image):
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._imageinfo = self._get_image_information()
        self._filesystem = self._attach_filesystem()
        self._filesysteminfo = {}

        if str_to_bool(self.get_parameter('discover')):
            self._built_filesystem_information()

    def get_folder_information(self, folderpath):
        if folderpath not in self._filesysteminfo.keys():
            folderinfo = FolderInfo(folderpath=folderpath, folderitems=set(self._discover_folder(folderpath)),
                                    imagefile=self._imagefilepath)
            self._filesysteminfo[folderpath] = folderinfo
            return folderinfo
        else:
            return self._filesysteminfo[folderpath]

    def get_partition_table(self):
        try:
            attr_id = getattr(pytsk3, f"TSK_VS_TYPE_{self.PARTITION_TYPE[self._fs_type]}")
            volume = pytsk3.Volume_Info(self._imageinfo, attr_id)
        except IOError as ioerror:
            _, e, _ = sys.exc_info()
            self._logger.info(f"Unable to read partition table.")
            raise ioerror

    def get_image_metadata(self):
        headers = self._imageinfo.ewf_handle.get_header_values()
        hashes = self._imageinfo.ewf_handle.get_hash_values()
        metadata = EWFMetadata(hashes=hashes, headers=headers,
                               bytes_per_sector=self._imageinfo.ewf_handle.bytes_per_sector,
                               number_of_sectors=self._imageinfo.ewf_handle.get_number_of_sectors(),
                               image_size=self._imageinfo.ewf_handle.get_media_size())

        return metadata

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
            raise TypeError("EWFImage can only hanlde ewf files (.e01).")

        return img_info

    def _attach_filesystem(self):
        fs = None

        for fs_type in self.FILE_SYSTEM_OFFSETS.keys():
            try:
                fs = pytsk3.FS_Info(self._imageinfo, self.FILE_SYSTEM_OFFSETS[fs_type])
                self._fs_type = fs_type
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
            offset = f.info.fs_info.offset

            yield FolderItemInfo(name=name, itemtype=f_type, size=size, create=create, modify_date=modify,
                                 offset=offset)

    # TODO Could potentially be speed up by using a set instead of a list for the folder info objects
    def _built_filesystem_information(self, folderpath='/'):
        folderinfo = self.get_folder_information(folderpath)
        self._filesysteminfo[folderpath] = folderinfo

        for item in folderinfo:
            if item.Type == "DIR" and item.Name != b'.' and item.Name != b'..':
                self._built_filesystem_information(f"{folderpath}{item.Name.decode()}/")


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

    @property
    def ewf_handle(self):
        return self._ewf_handle


class EWFMetadata:
    def __init__(self, headers, hashes, bytes_per_sector, number_of_sectors, image_size):
        self._headers = headers
        self._hashes = hashes
        self._bytes_per_sector = bytes_per_sector
        self._number_of_sectors = number_of_sectors
        self._image_size = image_size

    def __str__(self):
        result = ""
        for header, value in self._headers.items():
            result += f"\r\n{header}: {value}"

        for imghash, value in self._hashes.items():
            result += f"\r\n{imghash}: {value}"

        result += f"\r\nBytes per Sector: {self._bytes_per_sector}\r\n" \
                  f"Number of Sectors: {self._number_of_sectors}\r\nImage Size: {self._image_size}"

        return result
