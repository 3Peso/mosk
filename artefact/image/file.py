import logging

from baseclasses.artefact import ArtefactBase


class File(ArtefactBase):
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._partition_index = self.get_parameter('partitionindex')
        self._file_path = self.get_parameter('filepath')
        self._out_path = self.get_parameter('outpath')
        self._filename = self.get_parameter('filename')

    def _collect(self):
        try:
            self._parent.export_file(partitionindex=self._partition_index, filepath=self._file_path,
                                     outpath=self._out_path, filename=self._filename)
        except FileNotFoundError:
            self._logger.warning(f"Could not find file '{self._file_path}.'")
        except FileExistsError:
            self._logger.warning(f"File not exported, because file '{self._file_path}' already exists in "
                                 f"'{self._out_path}'.")

        self.data = f"File '{self._file_path}{self._filename}' exported to path '{self._out_path}'."