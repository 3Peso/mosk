__author__ = '3Peso'
__all__ = ['EWFImage', 'EWFImageInfo']

import logging
import pytsk3
import pyewf
import os
from logging import Logger
from contextlib import suppress
from functools import lru_cache

from source.baseclasses.image import Image, FolderInfo, FolderItemInfo
from businesslogic.support import str_to_bool, format_bytes
from businesslogic.errors import CollectorParameterError


class EWFPartition:
    def __init__(self, partition, fs_object) -> None:
        self.partition: dict = partition
        self._fs_object: pytsk3.FS_Info = fs_object

    def fs_object_initialized(self) -> bool:
        return self._fs_object is not None

    @property
    def fs_object(self) -> pytsk3.FS_Info:
        if self._fs_object is not None:
            return self._fs_object
        else:
            raise LookupError(f"Filesystem for partiton is unkown.")


class EWFImageInfo(pytsk3.Img_Info):
    def __init__(self, ewf_handle: pyewf.handle) -> None:
        self._ewf_handle: pyewf.handle = ewf_handle
        super(EWFImageInfo, self).__init__(url="",
                                           type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self) -> None:
        self._ewf_handle.close()

    def read(self, offset, size) -> str:
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self) -> int:
        return self._ewf_handle.get_media_size()

    @property
    def ewf_handle(self) -> pyewf.handle:
        return self._ewf_handle


class EWFMetadata:
    def __init__(self, headers: dict, hashes: dict, bytes_per_sector: int, number_of_sectors: int, image_size: str) \
            -> None:
        self._headers: dict = headers
        self._hashes: dict = hashes
        self._bytes_per_sector: int = bytes_per_sector
        self._number_of_sectors: int = number_of_sectors
        self._image_size: str = image_size

    def __str__(self) -> str:
        result: str = ""
        for header, value in self._headers.items():
            result += f"\r\n{header}: {value}"

        for imghash, value in self._hashes.items():
            result += f"\r\n{imghash}: {value}"

        result += f"\r\nBytes per Sector: {self._bytes_per_sector}\r\n" \
                  f"Number of Sectors: {self._number_of_sectors}\r\nImage Size: {self._image_size}"

        return result


class EWFPartitionTable:
    def __init__(self, volume: pytsk3.Volume_Info) -> None:
        self._volume: pytsk3.Volume_Info = volume

    def __str__(self) -> str:
        rowformat: str = "{:<9}{:<32}{:<21}{:<21}"
        result: str = rowformat.format('Index', 'Type', 'Offest Start Sector', 'Lenght in Sectors') + "\r\n\r\n"

        for partition in self._volume:
            result += \
                rowformat.format(partition.addr, partition.desc.decode('UTF-8'), partition.start, partition.len) + \
                "\r\n"

        return result


class EWFImage(Image):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._imageinfo: EWFImageInfo = self._get_image_information()
        self._initialize_partition_lookup()
        self._filesysteminfo: dict = {}
        self._fs_discoverd: bool = False
        if str_to_bool(self.get_parameter('discover')):
            self._fs_discoverd = True
            self._initialize_partitions()

    @property
    def filesysteminfo(self) -> dict:
        """
        Dictionary containing partitions and their content / files.
        :return:
        """
        if not self._fs_discoverd:
            raise CollectorParameterError("You can only export files with parameter 'discover' set to True during "
                                          "image object creation.")
        return self._filesysteminfo

    def get_folder_information(self, folderpath: str, partitionindex: int) -> FolderInfo:
        """
        Gets a FolderInfo object if the source partition contains the folder.
        :param folderpath: Path of the folder for which the folder info is request.
        :param partitionindex:
        """
        folderinfo: FolderInfo = None
        try:
            if folderpath not in self.filesysteminfo[partitionindex].keys():
                folderinfo: FolderInfo = FolderInfo(folderpath=folderpath,
                                                    folderitems=set(self._discover_folder(folderpath, partitionindex)),
                                                    imagefile=self._imagefilepath, partitionindex=partitionindex)
            else:
                folderinfo: FolderInfo = self.filesysteminfo[partitionindex][folderpath]
        except KeyError:
            folderinfo: FolderInfo = FolderInfo(folderpath=folderpath,
                                                folderitems=set(self._discover_folder(folderpath, partitionindex)),
                                                imagefile=self._imagefilepath, partitionindex=partitionindex)

        return folderinfo

    def get_partition_table(self) -> EWFPartitionTable:
        """
        Creates an EWFPartitionTable object containing all the partitions included in the image file.
        """
        return EWFPartitionTable(volume=self._get_volume_from_image())

    def get_image_metadata(self) -> EWFMetadata:
        """
        Retrieves all available metadata of the image and returns a EWFMetadata object.
        """
        headers: dict = self._imageinfo.ewf_handle.get_header_values()
        hashes: dict = self._imageinfo.ewf_handle.get_hash_values()
        metadata: EWFMetadata = EWFMetadata(hashes=hashes, headers=headers,
                                            bytes_per_sector=self._imageinfo.ewf_handle.bytes_per_sector,
                                            number_of_sectors=self._imageinfo.ewf_handle.get_number_of_sectors(),
                                            image_size=format_bytes(self._imageinfo.ewf_handle.get_media_size()))

        return metadata

    def export_file(self, filepath: str, filename: str, outpath: str) -> None:
        """
        Tries to export a file from the image file.
        Will try to find file with path and name in every partition in the provided image.
        :param filepath:
        :param filename:
        :param outpath: Outputpath for the exported file.
        :return: Nothing, but will copy the exported file to the output path. The partition index will be
        append to the output path as folder.
        """
        logger: Logger = logging.getLogger(__name__)
        fs_objects: list = list(self._get_fs_object(path=filepath, file=filename))
        if fs_objects is not None:
            for partitionindex, fso in fs_objects:
                try:
                    self._write_file(fso, filename, filepath, outpath, partitionindex)
                except OSError as oserror:
                    logger.error(f"Could not extract file from image.\r\n{oserror}")
        else:
            raise FileNotFoundError(f"Could not find '{filepath}{filename}' in image '{self._imagefilepath}'.")

    def get_file_stream(self, filepath: str, filename: str, buffer_size: int) -> bytes:
        """
        Yields a stream to go over a file in the image file to, for example, calculate the hash
        of the file without the need to export the file before hash calculation.
        :param filepath:
        :param filename:
        :param buffer_size: Size of the file chunks retunred by the genexp.
        :return:
        """
        logger: Logger = logging.getLogger(__name__)
        fs_objects: list = list(self._get_fs_object(path=filepath, file=filename))
        if fs_objects is not None:
            for partitionindex, fso in fs_objects:
                try:
                    return self._get_file_stream(fso, filename, filepath, partitionindex, buffer_size=buffer_size)
                except OSError as oserror:
                    logger.error(f"Could not aquire filestream from image.\r\n{oserror}")
        else:
            raise FileNotFoundError(f"Could not find '{filepath}{filename}' in image '{self._imagefilepath}'.")

    def _initialize_partitions(self) -> None:
        """
        Try to build a file system representatio of every partition in the provided image.
        """
        for partitionindex in range(0, len(self._partitions)):
            if self._partitions[partitionindex].fs_object_initialized():
                self._built_filesystem_information(partitionindex=partitionindex)

    def _initialize_partition_lookup(self) -> None:
        """
        Initializes a lookup table with all the partitions in the EWF image, as long as the partition
        filesystem can be interpreted by libtsk.
        :return: Will initialize the member _partitions.
        """
        self._volume: pytsk3.Volume_Info = self._get_volume_from_image()
        tmp: list = list(self._volume)
        self._partitions: dict = {paritionindex: self._get_partition_object(tmp[paritionindex])
                                  for paritionindex in range(0, len(tmp))}

    def _get_partition_object(self, partition: pytsk3.TSK_VS_PART_INFO) -> EWFPartition:
        """
        Builds an EWFPartition object containing the fs_object object for accessing files
        in the partition.
        :param partition:
        :return: EWFPartition object which contains an fs_object object needed to access files
        of this partition later
        """
        logger: Logger = logging.getLogger(__name__)
        fs: pytsk3.FS_Info = None
        try:
            fs = pytsk3.FS_Info(self._imageinfo, offset=partition.start * self._volume.info.block_size)
        except IOError as ioerror:
            logger.info(f"Unable to open FS:\r\n{ioerror}")

        partition_object = EWFPartition(partition=partition, fs_object=fs)

        return partition_object

    def _get_fs_object(self, path: str, file: str) -> [int, pytsk3.File]:
        """
        Yields a list object containing a pytsk3.File object for every found file in image for path
        and file(name). Checks every partition found in the image for the path and file.
        :param path: Path of the file.
        :param file: Name of the file with extension.
        :return: [partitionindex, pytsk3.File object]
        """
        logger = logging.getLogger(__name__)
        for partitionindex, partition in self._partitions.items():
            filecontent: pytsk3.File = None
            directory: pytsk3.Directory = None
            try:
                directory = partition.fs_object.open_dir(path=path)
                logger.debug(f"Path '{path}' exists in partiton #{partitionindex}.")
            except LookupError:
                logger.info(f"Filesystem of partition #{partitionindex} cannot be interpreted.")
            except OSError:
                logger.info(f"Path '{path}' not found in partition #{partitionindex}")

            if directory is not None:
                filecontent = self._get_filecontent(directory, file)
                if filecontent is not None:
                    yield [partitionindex, filecontent]

    @staticmethod
    def _get_filecontent(directory: pytsk3.Directory, file: str) -> pytsk3.File:
        """
        Checks every object in the directory to see if it has the file(name).
        :param directory: directory object
        :param file: file name with extension
        :return: pytsk3.File object
        """
        result: pytsk3.File = None
        for fs_object in directory:
            if hasattr(fs_object, "info") and \
                    hasattr(fs_object.info, "name") and \
                    hasattr(fs_object.info.name, "name"):
                if fs_object.info.name.name.decode('UTF-8') == file:
                    result = fs_object
                    break

        return result

    @classmethod
    def _write_file(cls, fs_object: pytsk3.File, filename: str, path: str, outputpath: str, partitionindex: int) \
            -> None:
        """
        Writes a file from an image to the local filesystem into the provided outpath. If this outpath does not
        exist, the outpath will be created before exporting the file. The final outpath will be the
        outpath + partitionindex + the path of the file in the image + the filename itself.
        :param fs_object: pytsk3.File object
        :param filename:
        :param path: the file path of the file to be exported, which it has in the image.
        :param outputpath: Path to the local file system where the exported file will be written to.
        """
        output_dir: str = os.path.join(os.path.join(outputpath, str(partitionindex)),
                                       os.path.dirname(path.lstrip("//")))
        buffer_size: int = 1024 * 1024
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        offset: int = 0
        size: int = fs_object.info.meta.size
        while offset < size:
            available_to_read = min(buffer_size, size - offset)
            data = fs_object.read_random(offset, available_to_read)
            if not data:
                break
            with open(os.path.join(output_dir, filename), "wb") as outfile:
                outfile.write(data)

            offset = offset + len(data)

    @classmethod
    def _get_file_stream(cls, fs_object: pytsk3.File, filename: str, path: str, partitionindex: int, buffer_size: int) \
            -> bytes:
        """
        Yields bytes stream to an object inside of an ewf image.
        :param fs_object:
        :param filename:
        :param path:
        :param partitionindex:
        :param buffer_size:
        :return:
        """
        offset: int = 0
        size: int = fs_object.info.meta.size
        while offset < size:
            available_to_read = min(buffer_size, size - offset)
            data = fs_object.read_random(offset, available_to_read)
            if not data:
                break
            offset = offset + len(data)

            yield data

    def _get_volume_from_image(self) -> pytsk3.Volume_Info:
        """
        Tries to get a Volume_Info object from the provided image file.
        :return: pytsk3.Volume_Info
        """
        logger: Logger = logging.getLogger(__name__)
        try:
            attr_id: int = getattr(pytsk3, f"TSK_VS_TYPE_{self._fstype}")
            volume: pytsk3.Volume_Info = pytsk3.Volume_Info(self._imageinfo, attr_id)
        except IOError:
            try:
                # Give it another try without a type. Maybe the provided type was wrong.
                logger.info(f"Could not open volume with the type '{self._fstype}'. Trying without type...")
                volume = pytsk3.Volume_Info = pytsk3.Volume_Info(self._imageinfo)
            except IOError as ioerror:
                logger.info(f"Unable to read partition table.")
                raise ioerror

        with suppress(Exception):
            self._logger.info(f"Volume is of type '{volume.info.vstype}'.")

        return volume

    def _get_image_information(self) -> EWFImageInfo:
        """
        Creates an EWFImageInfo object which contains the pyewf.handle object for operations on the
        ewf image.
        :return: EWFImageInfo object
        """
        if self._imagetype == self.IMAGE_TYPE_EWF:
            try:
                filenames: list = pyewf.glob(self._imagefilepath)
            except IOError as ioerror:
                self._logger.error(f"Invalid EWF format:\n{ioerror}")
                raise ioerror

            ewf_handle: pyewf.handle = pyewf.handle()
            ewf_handle.open(filenames)
            img_info = EWFImageInfo(ewf_handle)
        else:
            raise TypeError(f"EWFImage can only hanlde ewf files ({self.IMAGE_TYPE_EWF.FileEnding}).")

        return img_info

    def _discover_folder(self, folder: str, partitionindex: int) -> FolderItemInfo:
        """
        Yields a FolderItemInfo object for every item in the folder.
        :param folder: Path of the folder.
        :param partitionindex: Index of the partition where the folder can be found.
        """
        logger: Logger = logging.getLogger(__name__)
        if self._partitions[partitionindex].fs_object is not None:
            root_dir: pytsk3.Directory = self._partitions[partitionindex].fs_object.open_dir(path=folder)

            logger.debug(f"'{folder}' loading info from image ...")
            for f in root_dir:
                name: bytes = f.info.name.name
                if hasattr(f.info.meta, "type"):
                    if f.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                        f_type: str = "DIR"
                    else:
                        f_type: str = "FILE"
                    size: int = f.info.meta.size
                    create: int = f.info.meta.crtime
                    modify: int = f.info.meta.mtime
                    if hasattr(f.info.fs_info, "offset"):
                        offset: int = f.info.fs_info.offset
                    else:
                        offset: int = 0

                    yield FolderItemInfo(name=name, itemtype=f_type, size=size, create=create, modify_date=modify,
                                         offset=offset)

    @lru_cache()
    def _built_filesystem_information(self, folderpath='/', partitionindex=0) -> None:
        """
        Recursivly discovers the filesystem of a partition, decalred by its index. Initializes the
        member _filesystem on the go.
        :param folderpath: Current folder which is being trafersed.
        :param partitionindex: Index of the partition for which the filesystem information is been build.
        """
        partition: dict = None
        try:
            partition = self.filesysteminfo[partitionindex]
        except KeyError:
            partition = {}
            self.filesysteminfo[partitionindex] = partition

        folderinfo: FolderInfo = self.get_folder_information(folderpath, partitionindex)
        partition[folderpath] = folderinfo

        if folderinfo is not None:
            for item in folderinfo:
                if item.Type == "DIR" and item.Name != b'.' and item.Name != b'..':
                    self._built_filesystem_information(f"{folderpath}{item.Name.decode()}/", partitionindex)
