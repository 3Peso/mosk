from unittest import TestCase, mock
from unittest.mock import MagicMock

from artefact.localhost.osinformation import OSName


class TestOSNameCollect(TestCase):
    def test__collect(self):
        """
        Should return the macOS platform name for a platform version, which is known.
        :return:
        """
        expected_platform_name = "Yosemite"
        with mock.patch('artefact.localhost.osinformation.platform.mac_ver', MagicMock(return_value=['10.10'])):
            collector = OSName(parent=None, parameters={})
            collector._collect()
            actual_platform_name = collector.data[0].collecteddata

        self.assertEqual(expected_platform_name, actual_platform_name)

    def test__collect_platform_is_bigsur(self):
        """
        Should return always BigSur for all possible revisions of it.
        :return:
        """
        expected_platform_name = "BigSur"
        with mock.patch('artefact.localhost.osinformation.platform.mac_ver', MagicMock(return_value=['11.2.3'])):
            collector = OSName(parent=None, parameters={})
            collector._collect()
            actual_platform_name = collector.data[0].collecteddata

        self.assertEqual(expected_platform_name, actual_platform_name)

    def test__collect_platform_is_monterey(self):
        """
        Should return always Monterey for all possible revisions of it.
        :return:
        """
        expected_platform_name = "Monterey"
        with mock.patch('artefact.localhost.osinformation.platform.mac_ver', MagicMock(return_value=['12'])):
            collector = OSName(parent=None, parameters={})
            collector._collect()
            actual_platform_name = collector.data[0].collecteddata

        self.assertEqual(expected_platform_name, actual_platform_name)

    def test__collect_unkwon_platform(self):
        """
        Should collect a string saying, that the platform name cannot be collected.
        :return:
        """
        expected_platform_name = "Cannot collect OS name for platform version '13'"
        with mock.patch('artefact.localhost.osinformation.platform.mac_ver', MagicMock(return_value=['13'])):
            collector = OSName(parent=None, parameters={})
            collector._collect()
            actual_platform_name = collector.data[0].collecteddata

        self.assertEqual(expected_platform_name, actual_platform_name)

    def test__collection_version_string_unkown_format(self):
        """
        Should raise an exception
        :return:
        """
        expected_platform_name = "Cannot collect OS name. Unexpected version string format '1.1.1'."
        with mock.patch('artefact.localhost.osinformation.platform.mac_ver', MagicMock(return_value=['1.1.1'])):
            collector = OSName(parent=None, parameters={})
            collector._collect()
            actual_platform_name = collector.data[0].collecteddata

        self.assertEqual(expected_platform_name, actual_platform_name)


class TestOSNameSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.osinformation import OSName
        collector = OSName(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedplatform)

class TestOSVersionSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin".
        :return:
        """
        from artefact.localhost.osinformation import OSVersion
        collector = OSVersion(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedplatform)