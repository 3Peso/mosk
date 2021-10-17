import platform
from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestSourceLocalhostExpandFilepath(TestCase):
    @patch('source.localhost.Path.home', MagicMock(return_value='/home/someuser'))
    def test_expandfilepath_home_in_path(self):
        """
        Should expand '~' to the home path of the current user.
        """
        import source.localhost
        actual_expanded_path = source.localhost.expandfilepath('~/test')
        expected_path = '/home/someuser/test'
        if platform.system() == "Windows":
            expected_path = '/home/someuser\\test'

        self.assertEqual(expected_path, actual_expanded_path)

    def test_expandfilepath_no_home_in_path(self):
        """
        Should do nothing if there is no '~' in the path.
        """
        import source.localhost
        actual_expanded_path = source.localhost.expandfilepath('/somepath/test')
        expected_path = '/somepath/test'

        self.assertEqual(expected_path, actual_expanded_path)

    def test_expandfilepath_filepath_starts_with_slash(self):
        """
        Should expand '~' to the homepath of the current user.
        :return:
        """
        import source.localhost
        expected_path = '/home/somepath/test'
        if platform.system() == "Windows":
            expected_path = '/home/somepath\\test'
        with patch('source.localhost.Path.home', MagicMock(return_value="/home/somepath")):
            actual_path = source.localhost.expandfilepath('/~/test')

        self.assertEqual(expected_path, actual_path)

