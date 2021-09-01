from unittest import TestCase


class TestOSNameCollect(TestCase):
    def test__collect(self):
        """
        Should return the macOS platform name for a platform version, which is known.
        :return:
        """
        self.fail()

    def test__collect_platform_is_bigsur(self):
        """
        Should return always BigSur for all possible revisions of it.
        :return:
        """
        self.fail()

    def test__collect_platform_is_monterey(self):
        """
        Should return always Monterey for all possible revisions of it.
        :return:
        """
        self.fail()

    def test__collect_unkwon_platform(self):
        """
        Should collect a string saying, that the platform name cannot be collected.
        :return:
        """
        self.fail()

    def test__collection_version_string_unkown_format(self):
        """
        Should raise an exception
        :return:
        """
        self.fail()
