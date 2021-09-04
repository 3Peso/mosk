from unittest import TestCase


class TestNVRAMCollectorSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import NVRAMCollector
        collector = NVRAMCollector(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedsystem)

class TestLocalTimeSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import LocalTime
        collector = LocalTime(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedsystem)

class TestDetectFusionDriveSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import DetectFusionDrive
        collector = DetectFusionDrive(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedsystem)

class TestDetectFileFaultSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import DetectFileByName
        collector = DetectFileByName(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedsystem)


class TestDetectFileByNameSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import DetectFileByName
        collector = DetectFileByName(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedsystem)


class TestInstalledApplicationsSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import InstalledApplications
        collector = InstalledApplications(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedsystem)


class TestFileSystemInformationSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import FileSystemInformation
        collector = FileSystemInformation(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedsystem)


class TestHardwareInformationSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.system import HardwareInformation
        collector = HardwareInformation(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedsystem)