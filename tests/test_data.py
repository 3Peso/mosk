import os
from unittest import TestCase


class TestCollectionData(TestCase):

    def setUp(self) -> None:
        self._currentdir = os.getcwd()
        os.chdir('..')

    def tearDown(self):
        os.chdir(self._currentdir)

    def test_get_collector_info_as_str(self):
        """
        :return: Should return a string with collector informormation prepended.
        """
        from businesslogic.data import CollectionData

        actual_parameters = {'Param1': 12, 'Param2': 'Test'}
        actual_data = CollectionData(data="Test data", collector_name="TestCollector",
                                     collector_parameters=actual_parameters)
        teststring = "Test String"
        expected = "Test String\r\n\r\nCollector: TestCollector\r\nParam1: '12'\r\nParam2: 'Test'"
        actual = actual_data.get_collector_info_as_str(teststring)

        self.assertEqual(actual, expected)

    def test_get_collector_info_as_str_no_params(self):
        """
        :return: should only prepend the collector name
        """
        from businesslogic.data import CollectionData

        actual_data = CollectionData(data="Test data", collector_name="TestCollector")
        teststring = "Test String"
        expected = "Test String\r\n\r\nCollector: TestCollector"
        actual = actual_data.get_collector_info_as_str(teststring)

        self.assertEqual(actual, expected)

    def test_get_collector_info_as_str_no_collector_name(self):
        """
        With no collector provided it should raise a ValueError
        """
        from businesslogic.data import CollectionData

        actual_parameters = {'Param1': 12, 'Param2': 'Test'}
        actual_data = CollectionData(data="Test data", collector_parameters=actual_parameters)
        teststring = "Test String"

        with self.assertRaises(ValueError):
            actual_data.get_collector_info_as_str(teststring)

    def test_get_collector_info_as_str_no_collector_name_and_no_params(self):
        """
        Should do nothing.
        """
        from businesslogic.data import CollectionData

        actual_data = CollectionData(data="Test data")
        expected = "Test String"

        actual = actual_data.get_collector_info_as_str(expected)

        self.assertEqual(actual, expected)
