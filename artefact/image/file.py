import logging
import os

from baseclasses.artefact import ArtefactBase
from source.baseclasses.image import FolderInfo


class File(ArtefactBase):
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_path = self.get_parameter('filepath')
        self._out_path = self.get_parameter('outpath')
        self._filename = self.get_parameter('filename')

    def _collect(self):
        try:
            self._parent.export_file(filepath=self._file_path, outpath=self._out_path, filename=self._filename)
        except FileNotFoundError:
            self._logger.warning(f"Could not find file '{self._file_path}.'")
        except FileExistsError:
            self._logger.warning(f"File not exported, because file '{self._file_path}' already exists in "
                                 f"'{self._out_path}'.")

        self.data = f"File '{self._file_path}{self._filename}' exported to path '{self._out_path}'."


class FolderInformation(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._folder = self.get_parameter('folder')
        self._partitionindex = self.get_parameter('partitionindex')

    def _collect(self):
        folderinfo = self._parent.get_folder_information(self._folder, int(self._partitionindex))
        self.data = str(folderinfo)


class CompleteFileSystemInfo(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._outpath = self.get_parameter('outpath')

    def _collect(self):
        if not os.path.exists(self._outpath):
            os.makedirs(self._outpath)

        outfilepath = os.path.join(self._outpath, "filesystem.csv")
        with open(outfilepath, "a") as outfile:
            outfile.write(FolderInfo.get_cvs_header() + '\r\n')
            folders = [folder for _, partition in self._parent.filesysteminfo.items()
                       for _, folder in partition.items()]
            for folder in folders:
                for item in folder.get_folder_items_in_csv_format():
                    outfile.write(item + '\r\n')
