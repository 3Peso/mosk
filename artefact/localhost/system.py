"""
mosk mac module for classes collecting os information.
"""

__version__ = '0.0.7'
__author__ = '3Peso'
__all__ = ['NVRAMCollector', 'LocalTime']

from baseclasses.artefact import ArtefactBase
from businesslogic.support import run_terminal_command


class NVRAMCollector(ArtefactBase):
    """
    Tries to access the NVRAM of a macOS installation and store its content.
    """
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._supportedsystem = 'Darwin'

    def _collect(self):
        nvramcontent = run_terminal_command('nvram', '-xp')
        self.data = nvramcontent
        self.data[-1].save_as_md5(nvramcontent)


class LocalTime(ArtefactBase):
    """
    Gets the local time of the macOS installation from '/etc/localtime'.
    """
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._supportedsystem = 'Darwin'

    def _collect(self):
        self.data = run_terminal_command('zdump', '/etc/localtime')
        self.data.sourcepath = '/etc/localtime'


class DetectFusionDrive(ArtefactBase):
    """
    Trys to detect Fusion drives.
    """
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._supportedsystem = 'Darwin'

    def _collect(self):
        result = run_terminal_command('diskutil', 'list')
        possible_fusion = 'Fusion' in result
        self.data = f"Possible Fusion Drive detected: {possible_fusion}\r\n\r\nDiskutil list:\r\n{result}"


class DetectFileByName(ArtefactBase):
    """
    Tries to find an app installation
    """
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._supportedsystem = 'Darwin'

    def _collect(self):
        filename = self.get_parameter('filename')
        result = run_terminal_command('mdfind', self._get_mdfind_parameter(filename))
        if result is None or result == "":
            self.data = f"Application '{filename}' not found."
        else:
            self.data = f"Application '{filename}' found.\r\n{result}"

    @classmethod
    def _get_mdfind_parameter(cls, filename):
        if '*' in filename:
            return f"kMDItemDisplayName == {filename}"
        else:
            return f"kMDItemFSName={filename}"
