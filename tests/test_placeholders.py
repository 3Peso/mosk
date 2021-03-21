from unittest import TestCase, mock
from unittest.mock import MagicMock

from businesslogic.placeholders import Placeholder


# TODO tests should be independed from each other. There should be no required call order. Currently there is no
# TODO setup or teardown for each test.
class TestPlaceholder(TestCase):
    _placeholder_test_file = "placeholder_file_test.json"

    @staticmethod
    @mock.patch('os.path', MagicMock(return_value=True))
    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    def test_set_globalplaceholderfile():
        """Set the global placeholder file and initialize the placeholders with the file content"""
        Placeholder.set_globalplaceholderfile('test.txt')

        assert Placeholder._globalplaceholderfile == 'test.txt'
        assert Placeholder._initialize_global_placeholders.called

    @staticmethod
    def test_get_globalplaceholerfile():
        """Return the default placeholder file, if no placeholder file has been provided."""
        actual_placeholder_file = Placeholder.get_globalplaceholderfile()

        assert actual_placeholder_file == Placeholder.GLOBAL_PLACEHOLDER_FILE_PATH

    def test_set_globalplaceholderfile_with_testfile(self):
        """
        Set the global placeholder file and initialize the placeholders with the file content
        with no mocking
        """
        Placeholder.set_globalplaceholderfile(self._placeholder_test_file)

        assert Placeholder._globalplaceholderfile == self._placeholder_test_file

    def test_get_placeholder_from_testfile(self):
        """
        Should return content of test file if key is in the file.
        """
        existing_placeholder = "client"
        expected_value = "Sgt Mustman"

        Placeholder.set_globalplaceholderfile(self._placeholder_test_file)
        actual_value = Placeholder.get_placeholder(existing_placeholder)

        assert actual_value == expected_value

    def test_get_placeholder_with_nonexisting_key(self):
        """Should raise KeyError if the placeholder does not exist."""
        with self.assertRaises(KeyError): Placeholder.get_placeholder('IDoNotExist')

    def test_get_placeholder_casesensitive(self):
        """Should raise KeyError because of case insitivity"""
        Placeholder.set_globalplaceholderfile(self._placeholder_test_file)
        exisiting_placeholder = "client"
        nonexisting_placeholder = "Client"
        expected_value = "Sgt Mustman"

        assert Placeholder.get_placeholder(exisiting_placeholder) == expected_value
        with self.assertRaises(KeyError): Placeholder.get_placeholder(nonexisting_placeholder)
