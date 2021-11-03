from unittest import TestCase


class TestRecentUserItemsCollect(TestCase):
    def test__collect_with_external_mdfind_copy(self):
        """
        Should return all files a user has opened in his or her home dir during the last 60 minutes.
        :return:
        """
        self.fail()


class TestRecentUserItemsDunderInit(TestCase):
    def test___init(self):
        """
        Should initialize attribute _mdfind_path.
        :return:
        """
        self.fail()


class TestRecentUserItemsMDFindPathGetter(TestCase):
    def test_mdfind_path_not_set(self):
        """
        Should return 'mdfind'.
        :return:
        """
        self.fail()


class TestRecentUserItemsMDFindPathSetter(TestCase):
    def test_mdfind_path_sinagure_does_not_match(self):
        """
        Should raise an exception.
        :return:
        """
        self.fail()

    def test_mdfind_path_does_not_exist(self):
        """
        Should not set _mdfind_path
        :return:
        """
        self.fail()

    def test_mdfind_path_empty(self):
        """
        Should set _mdfind_path to empty string
        :return:
        """
        self.fail()

    def test_mdfind_path_exists_and_sig_matches(self):
        """
        Should set _mdfind_path
        :return:
        """
        self.fail()
