"""
Module to retrieve system information from an image file
"""

from baseclasses.artefact import ArtefactBase

__author__ = "3Peso"
__all__ = []


class FolderInformation(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._folder = self.get_parameter('folder')

    def _collect(self):
        folderinfo = self._parent.get_folder_information(self._folder)
        self.data = str(folderinfo)


class ImageMetadata(ArtefactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        metadata = self._parent.get_image_metadata()
        self.data = str(metadata)
