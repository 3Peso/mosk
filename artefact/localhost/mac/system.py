import subprocess

from baseclasses.artefact import ArtefactBase


class NVRAMCollector(ArtefactBase):
    """
    Tries to access the NVRAM of a macOS installation and store its content.
    """
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'NVRAMCollector'
        self._collectionmethod = 'nvram -p'
        self._description = 'Collects the contents of the NVRAM by calling the bash command "nvram".'

    def collect(self):
        process = subprocess.Popen(['nvram', '-xp'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        nvramcontent = process.communicate()[0]
        self.data = nvramcontent
        self.data.save_as_md5(nvramcontent)

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description


class LocalTime(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'LocalTime'
        self._collectionmethod = 'zdump /etc/localtime'
        self._description = 'Collects the local date and time by reading the contents of\r\n' \
                             'of "/etc/localtime" with zdump.'

    def collect(self):
        process = subprocess.Popen(['zdump', '/etc/localtime'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True)
        self.data = process.communicate()[0]
        self.data.sourcepath = '/etc/localtime'
