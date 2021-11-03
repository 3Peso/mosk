import os
import os.path
import glob
import logging
import platform
import shutil
import unittest
from unittest import TestCase

from artefact.network.system import TimeFromNTPServer


class TestMoskIntegrationTest(TestCase):
    _specific_error_messages = {
        "TemperatureFromOpenWeatherDotCom - API Key not set":
            "Could not load query. Error: 'apikey not set.'."
    }

    _currentCWD = ""
    _expected_log_file = "integration_test_log.txt"

    def setUp(self) -> None:
        self._currentCWD = os.getcwd()
        os.chdir('..')

    def tearDown(self) -> None:
        self._cleanup_artefacts()
        os.chdir(self._currentCWD)

    def _cleanup_artefacts(self):
        logger = logging.getLogger(__name__)
        testfile_path = './test.txt_*'
        if platform.system() == 'Windows':
            testfile_path = '.\\test.txt_*'
        for test_dir in glob.glob(testfile_path):
            try:
                shutil.rmtree(test_dir)
                logger.info(f"Removed test directory '{test_dir}' during test tear down.")
            except Exception:
                logger.warning(f"Could not remove '{test_dir}'.")

        for test_dir in glob.glob('./test.xml*'):
            try:
                shutil.rmtree(test_dir)
                logger.info(f"Removed test directory '{test_dir}' during test tear down.")
            except Exception:
                logger.warning(f"Could not remove '{test_dir}'.")

        try:
            os.remove(self._expected_log_file)
            logger.info(f"Removed test protocol log '{self._expected_log_file}' during test tear down.")
        except FileNotFoundError:
            logger.info(f"No test protocol '{self._expected_log_file}. Nothing to delete.'")

    def test_run_integration_test(self):
        if platform.system() != "Windows":
            os.system(f"python3 ./mosk.py -g './global_placeholders.json' -i "
                      f"'./tests/instructions/integration_test.xml' -e tst -l Debug "
                      f"-p {self._expected_log_file}")
        else:
            os.system(f"python mosk.py -g 'global_placeholders.json' -i "
                      f"'.\\tests\\instructions\\integration_test.xml' -e tst -l Debug "
                      f"-p {self._expected_log_file}")

        self.assertTrue(os.path.exists(self._expected_log_file))
        length = 657
        if platform.system() == 'Windows':
            length = 770
        self.assertTrue(self._validate_protocol_log_file_length(expected_length=length))
        self.assertTrue(self._validate_protocol_log_file())

    def test_run_small_integration_test(self):
        if platform.system() != "Windows":
            os.system(f"python3 ./mosk.py -g './global_placeholders.json' -i "
                      f"'./tests/instructions/integration_test_small.xml' -e tst -l Debug "
                      f"-p {self._expected_log_file}")
        else:
            os.system(f"python .\\mosk.py -g 'global_placeholders.json' -i "
                      f"'.\\tests\\instructions\\integration_test_small.xml' -e tst -l Debug "
                      f"-p {self._expected_log_file}")

        self.assertTrue(os.path.exists(self._expected_log_file))
        length = 256
        if platform.system() == 'Windows':
            length = 249
        self.assertTrue(self._validate_protocol_log_file_length(expected_length=length))
        self.assertTrue(self._validate_protocol_log_file())

    @unittest.skipIf(platform.system() != "Darwin", "This test is only meant for macOS platforms.")
    def test_run_macos_collection_instructions(self):
        expected_log_file:str = "mac_artefacts_log.txt"
        os.system(f"python3 ./mosk.py -g './global_placeholders.json' -i "
                  f"'./examples/collect-mac-artefacts.xml' -e mac -l Debug "
                  f"-p {expected_log_file}")

        self.assertTrue(os.path.exists(expected_log_file))

    def _validate_protocol_log_file_length(self, expected_length):
        logger = logging.getLogger(__name__)
        with open(self._expected_log_file) as file_to_count:
            num_lines = sum(1 for line in file_to_count)
        logger.info(f"Log file length: {num_lines}")
        print(f"expected length: {expected_length} - actual length: {num_lines}")
        return True if expected_length == num_lines else False

    def _validate_protocol_log_file(self):
        valid: bool = True
        logger = logging.getLogger(__name__)
        with open(self._expected_log_file) as logfile:
            logfile_lines = logfile.readlines()

        no_title = self._log_lines("No-Title-Line", self._find_lines(logfile_lines, "Title: None\n"),
                                   logger)
        no_title = self._log_lines('No-Title-Line', self._find_lines(logfile_lines, "Title: No Title Found"),
                                   logger)

        no_method = self._log_lines("No-Method-Line", self._find_lines(logfile_lines, "Collection Method: None\n"),
                                    logger)
        no_method = self._log_lines("No-Method-Line", self._find_lines(logfile_lines,
                                                                       "Collection Method: "
                                                                       "No Collection Method Found\n"),
                                    logger)

        no_description = self._log_lines("No-Description-Line", self._find_lines(logfile_lines, "Description: None\n"),
                                         logger)
        no_description = self._log_lines("No-Description-Line", self._find_lines(logfile_lines,
                                                                                 "Description: No Description Found\n"),
                                         logger)

        unhandled_exceptions = self._log_lines("Unhandled-Exception-Line", self._find_lines(logfile_lines,
                                               "Caught unhandled exception during collection of artefact."), logger)
        specific_error = self._check_for_specific_error_messages(logfile_lines, logger)

        valid = False if no_title or no_method or no_description or unhandled_exceptions or specific_error else True

        return valid

    def _check_for_specific_error_messages(self, logfile_lines, logger):
        found_error: bool = False
        for header in self._specific_error_messages:
            if self._log_lines(header, self._find_lines(logfile_lines, self._specific_error_messages[header]), logger):
                found_error = True
        return found_error

    @staticmethod
    def _find_lines(logfilecontent, line_text: str):
        no_title = []
        line_counter = 1
        for line in logfilecontent:
            if line == line_text or line.startswith(line_text):
                no_title.append(line_counter)
            line_counter += 1
        return no_title

    @staticmethod
    def _log_lines(header: str, lines, logger):
        lines_logged: bool = False

        for linenumber in lines:
            logger.warning(f"{header}: {linenumber}")
            lines_logged = True

        return lines_logged


class TestArtefactLocalhostFileFileMetadataCollectExtendedAttributes(TestCase):
    @unittest.skipIf(platform.system() == "Windows", "Platform currently not supported.")
    def test__collectExtendedAttributes_on_file_with_ext_attribs(self):
        """
        Should store the extended attributes in data
        :return:
        """
        from artefact.localhost.file import FileMetadata

        expected_data = "Extended Attributes: com.apple.FinderInfo\n"
        expected_filepath = "/opt/local/var/macports"
        collector: FileMetadata = FileMetadata(parameters={}, parent=None)
        collector.filepath = expected_filepath
        collector._collect_extended_attributes()

        actual_data = collector.data[-1].collecteddata

        self.assertEqual(expected_data, actual_data)


class TestTimeFromNTPServerCollect(TestCase):
    def test__collect(self):
        """
        Data should be initialized with NTPTime object.
        :return:
        """
        actual_collector = TimeFromNTPServer(parameters={'timeserver': '0.de.pool.ntp.org'}, parent=None)

        actual_collector._collect()

        self.assertIsInstance(actual_collector.data[0].collecteddata, str)

    def test__collect_no_ntp_server(self):
        """
        Should use default ntp server.
        :return:
        """
        expected_ntp_server = '0.de.pool.ntp.org'
        actual_collector = TimeFromNTPServer(parameters={}, parent=None)

        actual_collector._collect()

        self.assertEqual(actual_collector.timeserver, expected_ntp_server)
