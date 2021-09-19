from unittest import TestCase
from unittest.mock import patch


class TestSourceLocalhostExpandFilepath(TestCase):
    @patch('source.localhost.Path.home')
    @patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders')
    def test_expandfilepath_home_in_path(self, placeholder_mock, home_mock):
        """
        Should expand '~' to the home path of the current user.
        """
        import source.localhost
        home_mock.return_value = '/home/someuser'
        actual_expanded_path = source.localhost.expandfilepath('~/test')
        expected_path = '/home/someuser/test'

        self.assertEqual(expected_path, actual_expanded_path)

    @patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders')
    def test_expandfilepath_no_home_in_path(self, placeholder_mock):
        """
        Should do nothing if there is no '~' in the path.
        """
        import source.localhost
        actual_expanded_path = source.localhost.expandfilepath('/somepath/test')
        expected_path = '/somepath/test'

        self.assertEqual(expected_path, actual_expanded_path)
