from unittest import TestCase


class TestNVRAMCollectorSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import NVRAMCollector
        collector = NVRAMCollector(parameters={}, parent={})

        self.assertEqual("['Darwin']", str(collector.supported_platform))

class TestLocalTimeSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import LocalTime
        collector = LocalTime(parameters={}, parent={})

        self.assertEqual("['Darwin']", str(collector.supported_platform))

class TestDetectFusionDriveSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import DetectFusionDrive
        collector = DetectFusionDrive(parameters={}, parent={})

        self.assertEqual("['Darwin']", str(collector.supported_platform))

class TestDetectFileFaultSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import DetectFileByName
        collector = DetectFileByName(parameters={}, parent={})

        self.assertEqual("['Darwin']", str(collector.supported_platform))


class TestDetectFileByNameSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import DetectFileByName
        collector = DetectFileByName(parameters={}, parent={})

        self.assertEqual("['Darwin']", str(collector.supported_platform))


class TestInstalledApplicationsSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import InstalledApplications
        collector = InstalledApplications(parameters={}, parent={})

        self.assertEqual("['Darwin']", str(collector.supported_platform))


class TestFileSystemInformationSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import FileSystemInformation
        collector = FileSystemInformation(parameters={}, parent={})

        self.assertEqual("['Darwin']", str(collector.supported_platform))


class TestHardwareInformationSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import HardwareInformation
        collector = HardwareInformation(parameters={}, parent={})

        self.assertEqual("['Darwin']", str(collector.supported_platform))