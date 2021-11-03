import unittest
import platform
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
        Should throw an exeption
        :return:
        """
        from artefact.localhost.tools import PLUtil
        from businesslogic.errors import CollectorParameterError

        util = PLUtil(parameters={}, parent=None)
        self.assertRaises(CollectorParameterError, util._collect)

    def test__collect_filepath_points_to_file_with_wrong_format(self):
        """
        Data should contain message that states that the file format is wrong.
        :return:
        """
        from artefact.localhost.tools import PLUtil

        expected_message = "test.txt: Unexpected character T at line 1"
        util = PLUtil(parameters={}, parent=None)
        util.filepath = "./testfiles/test.txt"
        with patch('artefact.localhost.tools.run_terminal_command',
                  MagicMock(return_value="test.txt: Unexpected character T at line 1")):
            util._collect()

            self.assertEqual(expected_message, util.data[0].collecteddata)

    @unittest.skipIf(platform.system() != "Darwin", "Test only runs on macOS.")
    def test__collect_on_existing_plist_file(self):
        """
        Data should contain redable contents of the plist file.
        :return:
        """
        from artefact.localhost.tools import PLUtil

        expected_message = '"0db7d1adf349b912f612c9be06278706"\n'
        util = PLUtil(parameters={}, parent=None)
        util.filepath = "./testfiles/test.md5"
        #with patch('artefact.localhost.tools.run_terminal_command',
        #           MagicMock(return_value="test.txt: Unexpected character T at line 1")):
        util._collect()

        self.assertEqual(expected_message, util.data[0].collecteddata)

    def test__collect_no_tool_path_set(self):
        """
        Data should contain a warning, that the live "plutil" has been used at the last position.
        :return:
        """
        from artefact.localhost.tools import PLUtil

        expected_data = "WARNING: No own copy of 'PLUtil' provided. 'PLUtil' of the live artefact has been used."
        util = PLUtil(parameters={}, parent=None)
        util.filepath = "./testfiles/test.txt"
        util._tool_path = "plutil"
        with patch('artefact.localhost.tools.path.exists', MagicMock(return_value=True)):
            with patch('artefact.localhost.tools.run_terminal_command', MagicMock(return_value="")):
                util._collect()
                actual_data = util.data[-1].collecteddata

                self.assertEqual(expected_data, actual_data)



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
