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
