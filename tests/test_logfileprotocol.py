from unittest import TestCase
from unittest.mock import patch
from datetime import date
import os
import re


class TestLogFileProtocol(TestCase):
    def tearDown(self) -> None:
        filepattern = '^\d\d\d\d\d_tst_\d\d\d\d-\d\d-\d\d\.txt$'
        for f in os.listdir('.'):
            if re.search(filepattern, f):
                os.remove(os.path.join('.', f))

    def setUp(self) -> None:
        self.actual_filedate = date(day=26, month=5, year=2020)

    @patch('protocol.logfileprotocol.LogFileProtocol._get_current_file_counter')
    @patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders')
    def test_protocol_filename_counter_2(self, placeholder_mock, counter_mock):
        """
        Should return current log file name "00002_tst_2020-05-26.txt
        """
        from protocol.logfileprotocol import LogFileProtocol
        actual_tester = 'tst'
        counter_mock.return_value = 2
        actual_log_file_protocol_writer = LogFileProtocol(examiner=actual_tester, filedate=self.actual_filedate)
        expected_log_file_name = "00002_tst_2020-05-26.txt"

        self.assertEqual(expected_log_file_name, actual_log_file_protocol_writer.protocol_filename)

    @patch('protocol.logfileprotocol.glob')
    @patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders')
    def test_get_current_file_counter(self, placeholder_mock, glob_mock):
        """
        Should return 4 when there are three log file protocols in the directory
        """
        from protocol.logfileprotocol import LogFileProtocol
        glob_mock.return_value = ['00001_tst_2020-05-26.txt', '00002_tst_2020-05-26.txt', '00003_tst_2020-05-26.txt']
        actual_protocol = LogFileProtocol(examiner='tst', filedate=self.actual_filedate)
        actual_counter = actual_protocol._get_current_file_counter(actual_protocol._search_pattern)
        expected_counter = 4

        self.assertEqual(expected_counter, actual_counter)

    @patch('protocol.logfileprotocol.glob')
    @patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders')
    def test_get_current_file_counter(self, placeholder_mock, glob_mock):
        """
        Should raise an ValueError if there are 99999 protocols already.
        """
        from protocol.logfileprotocol import LogFileProtocol
        glob_mock.return_value = ['99999_tst_2020-05-26.txt']

        self.assertRaises(ValueError, LogFileProtocol._get_current_file_counter, '*')
