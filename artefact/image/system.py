"""
Module to retrieve system information from an image file
"""

__author__ = "3Peso"

from baseclasses.artefact import ArtefactBase


class ImageMetadata(ArtefactBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        metadata = self._parent.get_image_metadata()
        self.data = str(metadata)


class PartitionTable(ArtefactBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _collect(self) -> None:
        partition_table = self._parent.get_partition_table()
        self.data = str(partition_table)
