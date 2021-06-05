import os
import json
from datetime import datetime
from unittest import TestCase


class TestCollectionDataGetCollectorInfoAsStr(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._currentdir = os.getcwd()
        os.chdir('..')

    @classmethod
    def tearDownClass(cls) -> None:
        os.chdir(cls._currentdir)

    def test_get_collector_info_as_str(self):
        """
        :return: Should return a string with collector informormation prepended.
        """
        from businesslogic.data import CollectionData

        actual_parameters = {'Param1': 12, 'Param2': 'Test'}
        actual_data = CollectionData(data="Test data", collector_name="TestCollector")
        actual_data.collector_parameters = actual_parameters
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
        actual_data = CollectionData(data="Test data")
        actual_data.collector_parameters = actual_parameters
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


class TestCollectionDataGetCollectorInfoAsStr(TestCase):
    def test_get_json(self):
        """
        :return: JSON object of data object
        """
        from businesslogic.data import CollectionData

        actual_data = CollectionData(data="Test data")

        actual_json_string = actual_data.get_json()

        self.assertIsNotNone(actual_json_string)

    def test_get_json(self):
        """
        :return: JSON object of data object
        """
        from businesslogic.data import CollectionData

        expected_data = "Test data"
        expected_collector = "TestCollector"
        expected_collector_params = {
            "param1": "value1",
            "param2": "value2"
        }
        expected_sourcepath = "source_path"
        expected_sourcehash = "This is not a hash"
        actual_data_obj = CollectionData(data=expected_data, collector_name=expected_collector)
        actual_data_obj.collector_parameters = expected_collector_params
        actual_data_obj._sourcepath = expected_sourcepath
        actual_data_obj._sourcehash = expected_sourcehash
        expected_time = datetime.now()
        actual_data_obj.currentdatetime = expected_time

        actual_json_string = actual_data_obj.get_json()
        actual_json = json.loads(actual_json_string)

        self.assertIsNotNone(actual_json)
        self.assertIsNotNone(actual_json['CollectionTime'])
        self.assertEqual(actual_json['CollectionTime'], str(expected_time))
        self.assertEqual(actual_json['Data'], expected_data)
        self.assertEqual(actual_json['CollectorName'], expected_collector)
        self.assertEqual(actual_json['SourcePath'], expected_sourcepath)
        self.assertEqual(actual_json['SourceHash'], expected_sourcehash)
        self.assertEqual(actual_json['param1'], expected_collector_params['param1'])
        self.assertEqual(actual_json['param2'], expected_collector_params['param2'])


class TestCollectionDataDunderStr(TestCase):
    def test___str__(self):
        self.fail()

    def test___str__no_data(self):
        self.fail()


class TestCollectionDataSaveAsMd5(TestCase):
    def test_save_as_md5_data_smaller_than_4k(self):
        self.fail()

    def test_save_as_md5_data_zero(self):
        self.fail()

    def test_save_as_md5_bigger_than_4k(self):
        self.fail()


class TestCollectionDataSourcePath(TestCase):
    def test_sourcepath(self):
        self.fail()

    def test_sourcepath_does_not_exist(self):
        self.fail()

    def test_sourcepath_file_zero(self):
        self.fail()

    def test_sourcepath_file_not_accessible(self):
        self.fail()
