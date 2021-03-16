import subprocess

from baseclasses.artefact import ArtefactBase


class NVRAMCollector(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'NVRAMCollector'
        self.__collectionmethod = 'nvram -p'
        self.__description = 'Collects the contents of the NVRAM by calling the bash command "nvram".'

    def collect(self):
        process = subprocess.Popen(['nvram', '-p'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        self._collecteddata = process.communicate()[0]

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description