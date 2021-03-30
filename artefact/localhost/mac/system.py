"""
mosk mac module for classes collecting os information.
"""

__version__ = '0.0.4'
__author__ = '3Peso'
__all__ = ['NVRAMCollector', 'LocalTime']

import subprocess

from baseclasses.artefact import ArtefactBase


class NVRAMCollector(ArtefactBase):
    """
    Tries to access the NVRAM of a macOS installation and store its content.
    """
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)

    def _collect(self):
        process = subprocess.Popen(['nvram', '-xp'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        nvramcontent = process.communicate()[0]
        self.data = nvramcontent
        self.data[-1].save_as_md5(nvramcontent)

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description


class LocalTime(ArtefactBase):
    """
    Gets the local time of the macOS installation from '/etc/localtime'.
    """
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)

    def _collect(self):
        process = subprocess.Popen(['zdump', '/etc/localtime'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        self.data = process.communicate()[0]
        self.data.sourcepath = '/etc/localtime'
