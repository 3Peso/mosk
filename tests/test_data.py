from unittest import TestCase

from businesslogic.data import CollectionData


class TestCollectionData(TestCase):

    def test_get_collector_info_as_str(self):
        """
        :return: Should return a string with collector informormation prepended.
        """
        actual_parameters = {'Param1': 12, 'Param2': 'Test'}
        actual_data = CollectionData(data="Test data", collector_name="TestCollector",
                                     collector_parameters=actual_parameters)
        teststring = "Test String"
        expected = "Test String\r\n\r\nCollector: TestCollector\r\nParam1: '12'\r\nParam2: 'Test'"
        actual = actual_data.get_collector_info_as_str(teststring)

        assert actual == expected

    def test_get_collector_info_as_str_no_params(self):
        """
        :return: should only prepend the collector name
        """
        actual_data = CollectionData(data="Test data", collector_name="TestCollector")
        teststring = "Test String"
        expected = "Test String\r\n\r\nCollector: TestCollector"
        actual = actual_data.get_collector_info_as_str(teststring)

        assert actual == expected

    def test_get_collector_info_as_str_no_collector_name(self):
        """
        With no collector provided it should raise a ValueError
        """
        actual_parameters = {'Param1': 12, 'Param2': 'Test'}
        actual_data = CollectionData(data="Test data", collector_parameters=actual_parameters)
        teststring = "Test String"

        with self.assertRaises(ValueError):
            actual_data.get_collector_info_as_str(teststring)

    def test_get_collector_info_as_str_no_collector_name_and_no_params(self):
        """
        Should do nothing
        """
        actual_data = CollectionData(data="Test data")
        expected = "Test String"

        actual = actual_data.get_collector_info_as_str(expected)

        assert actual == expected
