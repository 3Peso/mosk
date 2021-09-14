"""
mosk mac module for classes collecting os information.
"""

__author__ = '3Peso'
__all__ = ['NVRAMCollector', 'LocalTime', 'DetectFileByName', 'DetectFusionDrive']

from baseclasses.artefact import MacArtefact
from businesslogic.support import run_terminal_command


class NVRAMCollector(MacArtefact):
    """
    Tries to access the NVRAM of a macOS installation and store its content.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        nvramcontent = run_terminal_command(['nvram', '-xp'])
        self.data = nvramcontent
        self.data[-1].save_as_md5(nvramcontent)


class LocalTime(MacArtefact):
    """
    Gets the local time of the macOS installation from '/etc/localtime'.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        self.data = run_terminal_command(['zdump', '/etc/localtime'])
        self.data[-1].sourcepath = '/etc/localtime'


class DetectFusionDrive(MacArtefact):
    """
    Trys to detect Fusion drives.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        result = run_terminal_command(['diskutil', 'list'])
        possible_fusion = 'Fusion' in result
        self.data = f"Possible Fusion Drive detected: {possible_fusion}\r\n\r\nDiskutil list:\r\n{result}"


class DetectFileVault(MacArtefact):
    """
    Trys to detect FileVaul encryption
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        result = run_terminal_command(['diskutil', 'apfs', 'list'])
        possible_filevault = 'FileVault:                 Yes' in result
        self.data = f"Possible FileVault encryption detected: " \
                    f"{possible_filevault}\r\n\r\nDiskutil apfs list: \r\n{result}"


class DetectFileByName(MacArtefact):
    """
    Tries to find a file, currently by the use of the CLI of spotlight 'mdfind'
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        filename = self.get_parameter('filename')
        result = run_terminal_command(['mdfind', self._get_mdfind_parameter(filename)])
        if result is None or result == "":
            self.data = f"Application '{filename}' not found."
        else:
            self.data = result

    @classmethod
    def _get_mdfind_parameter(cls, filename):
        if '*' in filename:
            return f"kMDItemDisplayName == {filename}"
        else:
            return f"kMDItemFSName={filename}"


class InstalledApplications(MacArtefact):
    """
    Retrieve all installed applications on a mac
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        self.data = run_terminal_command(['system_profiler', 'SPApplicationsDataType'])


class FileSystemInformation(MacArtefact):
    """
    Retrieve file system information with onboard tools
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        self.data = run_terminal_command(['diskutil', 'list'])
        self.data = run_terminal_command(['diskutil', 'apfs', 'list'])


class HardwareInformation(MacArtefact):
    """
    Uses the system profiler to collect serial number, model, firmware, etc. from a mac.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collect(self):
        self.data = run_terminal_command(['system_profiler', 'SPHardwareDataType'])
