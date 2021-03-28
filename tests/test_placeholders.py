from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

from businesslogic.placeholders import Placeholder


class TestPlaceholder(TestCase):
    _placeholder_test_file = "placeholder_file_test.json"

    def setUp(self) -> None:
        Placeholder._globalplaceholderfile = Placeholder.GLOBAL_PLACEHOLDER_FILE_PATH

    @mock.patch('os.path', MagicMock(return_value=True))
    def test_set_globalplaceholderfile(self):
        """Set the global placeholder file and initialize the placeholders with the file content"""
        with patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders') as init_mock:
            Placeholder.set_globalplaceholderfile('test.txt')

            self.assertEqual(Placeholder._globalplaceholderfile, 'test.txt')
            init_mock.assert_called()

    def test_get_globalplaceholerfile(self):
        """Return the default placeholder file, if no placeholder file has been provided."""
        actual_placeholder_file = Placeholder.get_globalplaceholderfile()

        self.assertEqual(actual_placeholder_file, Placeholder.GLOBAL_PLACEHOLDER_FILE_PATH)

    def test_set_globalplaceholderfile_with_testfile(self):
        """
        Set the global placeholder file and initialize the placeholders with the file content
        with no mocking
        """
        Placeholder.set_globalplaceholderfile(self._placeholder_test_file)

        self.assertEqual(Placeholder._globalplaceholderfile, self._placeholder_test_file)

    def test_get_placeholder_from_testfile(self):
        """
        Should return content of test file if key is in the file.
        """
        existing_placeholder = "client"
        expected_value = "Sgt Mustman"

        Placeholder.set_globalplaceholderfile(self._placeholder_test_file)
        actual_value = Placeholder.get_placeholder(existing_placeholder)

        self.assertEqual(actual_value, expected_value)

    def test_get_placeholder_with_nonexisting_key(self):
        """Should raise KeyError if the placeholder does not exist."""
        with self.assertRaises(KeyError):
            Placeholder.get_placeholder('IDoNotExist')

    def test_get_placeholder_casesensitive(self):
        """Should raise KeyError because of case insitivity"""
        Placeholder.set_globalplaceholderfile(self._placeholder_test_file)
        exisiting_placeholder = "client"
        nonexisting_placeholder = "Client"
        expected_value = "Sgt Mustman"

        self.assertEqual(Placeholder.get_placeholder(exisiting_placeholder), expected_value)
        with self.assertRaises(KeyError):
            Placeholder.get_placeholder(nonexisting_placeholder)

    def test__call__should_replace_placeholder_in_string(self):
        """Using the @Placeholder decorator on a function returing a string should replace placeholders in
        that string with the values stored in the placeholder dictionary."""
        Placeholder.set_globalplaceholderfile(self._placeholder_test_file)
        string_with_placeholder = "This was it! !@client@! had enough. 'This has to end now!', !@client@! thought."
        expected_string = "This was it! Sgt Mustman had enough. 'This has to end now!', Sgt Mustman thought."

        @Placeholder
        def test_function():
            return string_with_placeholder

        actual_string = test_function()

        self.assertEqual(actual_string, expected_string)
