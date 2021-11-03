from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestPLUtilCollectInit(TestCase):
    def test___init__(self):
        """
        Should initialize property tool_path with empty string.
        :return:
        """
        from artefact.localhost.tools import PLUtil

        expected_tool_path = ""
        util = PLUtil(parameters={}, parent=None)
        actual_tool_path = util._tool_path

        self.assertEqual(expected_tool_path, actual_tool_path)

class TestPLUtilCollect(TestCase):
    def test__collect_no_filepath_provided(self):
        """
        Data should contain message that the provided plist file does not exist.
        :return:
        """
        self.fail()

    def test__collect_filepath_points_to_file_with_wrong_format(self):
        """
        Data should contain message that states that the file format is wrong.
        :return:
        """
        self.fail()

    def test__collect_filepath_has_unsupported_extension(self):
        """
        Data should contain message, that the file extension is not supported.
        :return:
        """
        self.fail()

    def test__collect_on_existing_plist_file(self):
        """
        Data should contain redable contents of the plist file.
        :return:
        """
        self.fail()

    def test__collect_no_tool_path_set(self):
        """
        Data should contain a warning, that the live "plutil" has been used at position 1.
        :return:
        """
        self.fail()


class TestPLUtilGetToolPath(TestCase):
    def test_tool_path_with_empty__tool_path(self):
        """
        Should return 'plutil' indicating that the live plutil is used.
        :return:
        """
        from artefact.localhost.tools import PLUtil

        expected_tool_path = "plutil"
        util = PLUtil(parameters={}, parent=None)
        actual_tool_path = util.tool_path

        self.assertEqual(expected_tool_path, actual_tool_path)


class TestPLUtilSetToolPath(TestCase):
    @patch('artefact.localhost.tools.path.exists', MagicMock(return_value=True))
    def test_tool_path_existing_path(self):
        """
        Should return tool path.
        """
        from artefact.localhost.tools import PLUtil

        util = PLUtil(parameters={}, parent=None)
        with patch('artefact.localhost.tools.validate_file_signature', MagicMock(return_value=True)):
            expected_tool_path = "some_tool_path"
            util.tool_path = expected_tool_path
            actual_tool_path = util._tool_path

            self.assertEqual(expected_tool_path, actual_tool_path)

    def test_tool_path_is_empty(self):
        """
        Should set _tool_path to empty string.
        :return:
        """
        from artefact.localhost.tools import PLUtil

        expected_tool_path = ""
        util = PLUtil(parameters={}, parent=None)
        util.tool_path = ""
        actual_tool_path = util._tool_path

        self.assertEqual(expected_tool_path, actual_tool_path)

    @patch('artefact.localhost.tools.path.exists', MagicMock(return_value=True))

    def test_tool_path_exisiting_path_but_wrong_signature(self):
        """
        Should throw an exception.
        :return:
        """
        from artefact.localhost.tools import PLUtil
        from businesslogic.errors import SignatureMatchError

        util = PLUtil(parameters={}, parent=None)
        with patch('artefact.localhost.tools.validate_file_signature', MagicMock(return_value=False)):
            expected_util_path = 'some_tool_path'
            with self.assertRaises(SignatureMatchError):
                util.tool_path = expected_util_path
