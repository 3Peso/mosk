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
        self.data = process.communicate()[0]

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description


class LocalTime(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'LocalTime'
        self.__collectionmethod = 'zdump /etc/localtime'
        self.__description = 'Collects the local date and time by reading the contents of\r\n' \
                             'of "/etc/localtime" with zdump.'

    def collect(self):
        process = subprocess.Popen(['zdump', '/etc/localtime'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        self.data = process.communicate()[0]
        self.data.sourcepath = '/etc/localtime'

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description
