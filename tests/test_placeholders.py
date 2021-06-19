from unittest import TestCase, mock
from unittest.mock import MagicMock, patch

from businesslogic.placeholders import Placeholder


class TestPlaceholderSetPlaceholderFile(TestCase):
    _placeholder_test_file = "placeholder_file_test.json"

    def setUp(self) -> None:
        Placeholder._globalplaceholderfile = Placeholder.GLOBAL_PLACEHOLDER_FILE_PATH

    @mock.patch('os.path', MagicMock(return_value=True))
    def test_set_globalplaceholderfile(self):
        """Set the global placeholder file and initialize the placeholders with the file content"""
        with patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders') as init_mock:
            Placeholder.set_globalplaceholderfile('./testfiles/test.txt')

            self.assertEqual(Placeholder._globalplaceholderfile, './testfiles/test.txt')
            init_mock.assert_called()


class TestPlaceholderGetGlobalPlaceholderFile(TestCase):
    _placeholder_test_file = "placeholder_file_test.json"

    def setUp(self) -> None:
        Placeholder._globalplaceholderfile = Placeholder.GLOBAL_PLACEHOLDER_FILE_PATH

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


class TestPlaceholderGetPlaceholder(TestCase):
    _placeholder_test_file = "placeholder_file_test.json"

    def setUp(self) -> None:
        Placeholder._globalplaceholderfile = Placeholder.GLOBAL_PLACEHOLDER_FILE_PATH

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


class TestPlaceholderCall(TestCase):
    _placeholder_test_file = "placeholder_file_test.json"

    def setUp(self) -> None:
        Placeholder._globalplaceholderfile = Placeholder.GLOBAL_PLACEHOLDER_FILE_PATH

    def test__call__should_replace_placeholder_in_string(self):
        """Using the @Placeholder decorator on a function returing a string should replace placeholders in
        that string with the values stored in the placeholder dictionary."""
        Placeholder.set_globalplaceholderfile(self._placeholder_test_file)
        string_with_placeholder = f"This was it! {Placeholder.PLACEHOLDER_START}client{Placeholder.PLACEHOLDER_END} " \
                                  f"had enough. 'This has to end now!', " \
                                  f"{Placeholder.PLACEHOLDER_START}client{Placeholder.PLACEHOLDER_END} thought."
        expected_string = "This was it! Sgt Mustman had enough. 'This has to end now!', Sgt Mustman thought."

        @Placeholder
        def test_function():
            return string_with_placeholder

        actual_string = test_function()

        self.assertEqual(actual_string, expected_string)

    def test__call__no_placeholders(self):
        """
        Should to nothing with the text.
        """
        expected_string = "This is a string without a placeholder"

        @Placeholder
        def test_function():
            return expected_string

        actual_string = test_function()

        self.assertEqual(expected_string, actual_string)

    def test__call__only_rightmost_delimeter_of_a_placeholder(self):
        """
        Should do nothing with the text.
        """
        expected_string = f"This is a string without a placeholder{Placeholder.PLACEHOLDER_END}"

        @Placeholder
        def test_function():
            return expected_string

        actual_string = test_function()

        self.assertEqual(expected_string, actual_string)

    def test__call__only_leftmost_delimeter_of_a_placeholer(self):
        """
        Should do nothing with the text.
        """
        expected_string = f"This is a {Placeholder.PLACEHOLDER_START}string without a placeholder"

        @Placeholder
        def test_function():
            return expected_string

        actual_string = test_function()

        self.assertEqual(expected_string, actual_string)

    def test__call__left_and_right_delimeter_but_across_several_words(self):
        """
        Should do nothing with the text.
        """
        expected_string = f"This is a {Placeholder.PLACEHOLDER_START}string without a " \
                          f"{Placeholder.PLACEHOLDER_END} placeholder"

        @Placeholder
        def test_function():
            return expected_string

        actual_string = test_function()

        self.assertEqual(expected_string, actual_string)

    def test__call__right_and_left_delimeter_in_wrong_order(self):
        """
        Should do nothing with the text.
        """
        expected_string = f"This is a {Placeholder.PLACEHOLDER_END}string{Placeholder.PLACEHOLDER_START} " \
                          f"without a placeholder"

        @Placeholder
        def test_function():
            return expected_string

        actual_string = test_function()

        self.assertEqual(expected_string, actual_string)

    def test__call__empty_string(self):
        """
        Should to nothing with the text
        """
        expected_string = ""

        @Placeholder
        def test_function():
            return expected_string

        actual_string = test_function()

        self.assertEqual(expected_string, actual_string)


class TestPlaceholderReplacePlaceholders(TestCase):
    def test_replace_placeholders(self):
        """
        Should replace the placeholder inside the provided text, if the value for the placeholder has already been
        defined.
        """
        string_with_placeholder = f"This is a string with " \
                                  f"{Placeholder.PLACEHOLDER_START}placeholder{Placeholder.PLACEHOLDER_END}"
        placeholder_value = "Yabubabba!"
        Placeholder._instruction_placeholders["placeholder"] = placeholder_value
        expected_string = f"This is a string with {placeholder_value}"

        actual_string = Placeholder.replace_placeholders(string_with_placeholder)

        self.assertEqual(expected_string, actual_string)

    def test_replace_placeholders_no_placeholder(self):
        """
        Should do nothing.
        """
        expected_string = "This is a string with nothing"

        actual_string = Placeholder.replace_placeholders(expected_string)

        self.assertEqual(expected_string, actual_string)

    def test_replace_placeholders_empty_string(self):
        """
        Should do nothing.
        """
        expected_string = ""

        actual_string = Placeholder.replace_placeholders(expected_string)

        self.assertEqual(expected_string, actual_string)

    def test_replace_placeholders_unkwon_placeholder(self):
        """
        Should do nothing.
        """
        expected_string = f"This is a string with " \
                          f"{Placeholder.PLACEHOLDER_START}unkown{Placeholder.PLACEHOLDER_END}"

        actual_string = Placeholder.replace_placeholders(expected_string)

        self.assertEqual(expected_string, actual_string)


class TestPlaceholderInitializeGlobalPlaceholders(TestCase):
    def test__initialize_global_placeholders(self):
        pass


class TestPlaceholderUpdatePlaceholder(TestCase):
    def test_update_placeholder_with_new_placeholder(self):
        pass

    def test_update_placeholder_with_defined_placeholder(self):
        pass

    def test_update_placeolder_with_value_which_contains_placeholder(self):
        pass
