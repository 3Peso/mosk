from unittest import TestCase
from unittest.mock import MagicMock, patch
from datetime import date
import os
import re


class TestLogFileProtocol(TestCase):
    def tearDown(self) -> None:
        filepattern = '^\d\d\d\d\d_tst_\d\d\d\d-\d\d-\d\d\.txt$'
        for f in os.listdir('.'):
            if re.search(filepattern, f):
                os.remove(os.path.join('.', f))

    @patch('protocol.logfileprotocol.LogFileProtocol._get_current_file_counter')
    @patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders')
    def test_protocol_filename_counter_2(self, protocol_mock, counter_mock):
        """
        Should return current log file name "00002_tst_2020-05-26.txt
        """
        from protocol.logfileprotocol import LogFileProtocol
        actual_tester = 'tst'
        counter_mock.return_value = 2
        actual_filedate = date(day=26, month=5, year=2020)
        actual_log_file_protocol_writer = LogFileProtocol(examiner=actual_tester, filedate=actual_filedate)
        expected_log_file_name = "00002_tst_2020-05-26.txt"

        self.assertEqual(expected_log_file_name, actual_log_file_protocol_writer.protocol_filename)
