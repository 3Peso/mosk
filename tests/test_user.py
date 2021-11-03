from unittest import TestCase
from unittest.mock import patch, MagicMock

from businesslogic.errors import SignatureMatchError


class TestRecentUserItemsCollect(TestCase):
    def test__collect_with_external_mdfind_copy(self):
        """
        Should return all files a user has opened in his or her home dir during the last 60 minutes.
        :return:
        """
        from artefact.localhost.user import RecentUserItems

        expcted_files = "Recent User Files"
        recent = RecentUserItems(parameters={}, parent=None)
        with patch('artefact.localhost.user.subprocess.Popen.communicate',
                   MagicMock(return_value=(b'Recent User Files', ""))):
            recent._collect()
            actual_files = recent.data[-1].collecteddata

            self.assertEqual(expcted_files, actual_files)


class TestRecentUserItemsDunderInit(TestCase):
    def test___init(self):
        """
        Should initialize attribute _mdfind_path.
        :return:
        """
        from artefact.localhost.user import RecentUserItems

        expected_mdfind_path = ""
        recent = RecentUserItems(parameters={}, parent=None)
        actual_mdfind_path = recent._mdfind_path

        self.assertEqual(expected_mdfind_path, actual_mdfind_path)


class TestRecentUserItemsMDFindPathGetter(TestCase):
    def test_mdfind_path_not_set(self):
        """
        Should return 'mdfind'.
        :return:
        """
        from artefact.localhost.user import RecentUserItems

        expected_path = "mdfind"
        recent = RecentUserItems(parameters={}, parent=None)
        actual_path = recent.mdfind_path

        self.assertEqual(expected_path, actual_path)


class TestRecentUserItemsMDFindPathSetter(TestCase):
    @patch('artefact.localhost.user.path.exists', MagicMock(return_value=True))
    def test_mdfind_path_sinagure_does_not_match(self):
        """
        Should raise an exception.
        :return:
        """
        from artefact.localhost.user import RecentUserItems

        recent = RecentUserItems(parameters={}, parent=None)
        with patch('artefact.localhost.user.validate_file_signature', MagicMock(return_value=False)):
            with self.assertRaises(SignatureMatchError):
                recent.mdfind_path = "HelloWorld"

    def test_mdfind_path_does_not_exist(self):
        """
        Should not set _mdfind_path
        :return:
        """
        from artefact.localhost.user import RecentUserItems

        expected_path = ""
        recent = RecentUserItems(parameters={}, parent=None)
        recent.mdfind_path = "HelloWorld"
        actual_path = recent._mdfind_path

        self.assertEqual(expected_path, actual_path)

    def test_mdfind_path_empty(self):
        """
        Should set _mdfind_path to empty string
        :return:
        """
        from artefact.localhost.user import RecentUserItems

        expected_path = ""
        recent = RecentUserItems(parameters={}, parent=None)
        recent.mdfind_path = ""
        actual_path = recent._mdfind_path

        self.assertEqual(expected_path, actual_path)

    @patch('artefact.localhost.user.path.exists', MagicMock(return_value=True))
    def test_mdfind_path_exists_and_sig_matches(self):
        """
        Should set _mdfind_path
        :return:
        """
        from artefact.localhost.user import RecentUserItems

        expected_path = "MyFindTool"
        recent = RecentUserItems(parameters={}, parent=None)
        with patch('artefact.localhost.user.validate_file_signature', MagicMock(return_value=True)):
            recent.mdfind_path = expected_path
            actual_path = recent._mdfind_path

            self.assertEqual(expected_path, actual_path)