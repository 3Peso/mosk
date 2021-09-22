import os
import json
import platform
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch

from businesslogic.data import CollectionMetaData


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
        :return: Should return a string with collector informormation.
        """
        from businesslogic.data import CollectionData

        actual_parameters = {'Param1': 12, 'Param2': 'Test'}
        actual_data = CollectionData(data="Test data", collector_name="TestCollector")
        actual_data.collector_parameters = actual_parameters
        expected = "Collector: TestCollector\r\nParam1: '12'\r\nParam2: 'Test'"
        actual = actual_data.get_collector_info_as_str()

        self.assertEqual(actual, expected)

    def test_get_collector_info_as_str_no_params(self):
        """
        :return: should only prepend the collector name
        """
        from businesslogic.data import CollectionData

        actual_data = CollectionData(data="Test data", collector_name="TestCollector")
        expected = "Collector: TestCollector"
        actual = actual_data.get_collector_info_as_str()

        self.assertEqual(actual, expected)

    def test_get_collector_info_as_str_no_collector_name(self):
        """
        With no collector provided it should raise a ValueError
        """
        from businesslogic.data import CollectionData
        from businesslogic.errors import NoCollectorError

        actual_parameters = {'Param1': 12, 'Param2': 'Test'}
        actual_data = CollectionData(data="Test data")
        actual_data.collector_parameters = actual_parameters

        with self.assertRaises(NoCollectorError):
            actual_data.get_collector_info_as_str()

    def test_get_collector_info_as_str_no_collector_name_and_no_params(self):
        """
        Should do nothing.
        """
        from businesslogic.data import CollectionData

        actual_data = CollectionData(data="Test data")

        actual = actual_data.get_collector_info_as_str()

        self.assertEqual('', actual)


class TestCollectionDataGetJson(TestCase):
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
    @patch("businesslogic.data.CollectionData.get_metadata_as_str")
    @patch("businesslogic.data.CollectionData.get_collector_info_as_str")
    def test___str__(self, collector_info_mock, metadata_mock):
        """
        Should return

        -- Collection Data     ----------

        Test data

        -- Collection Metadata ----------

        Collection Time Stamp: Timestamp
        Source MD5: MD5Hash
        Source path: SourcePath

        Collector: Collector
        filepath: FilePath

        ---------------------------------
        """
        from businesslogic.data import CollectionData

        actual_data = CollectionData(collector_name="Collector", data="Test data")
        metadata_mock.return_value = "Collection Time Stamp: Timestamp\r\nSource MD5: MD5Hash\r\nSource Path: SourcePath"
        collector_info_mock.return_value = "Collector: Collector\r\nfilepath: FilePath"
        expected_string = '-- Collection Data     ----------\r\n\r\nTest data\r\n\r\n' \
                          '-- Collection Metadata ----------\r\nCollection Time Stamp: Timestamp\r\n' \
                          'Source MD5: MD5Hash\r\nSource Path: SourcePath\r\nCollector: Collector\r\n' \
                          'filepath: FilePath\r\n---------------------------------\r\n'

        self.assertEqual(expected_string, str(actual_data))

    @patch("businesslogic.data.CollectionData.get_metadata_as_str")
    @patch("businesslogic.data.CollectionData.get_collector_info_as_str")
    def test___str__no_data(self, collector_info_mock, metadata_mock):
        """
        Should return
        -- Collection Data     ----------

        *No data collected*

        -- Collection Metadata ----------

        Collection Time Stamp: Timestamp
        Source MD5: MD5Hash
        Source path: SourcePath

        Collector: Collector
        filepath: FilePath

        ---------------------------------
        :return:
        """
        from businesslogic.data import CollectionData

        actual_data = CollectionData(collector_name="Collector", data="")
        metadata_mock.return_value = "Collection Time Stamp: Timestamp\r\nSource MD5: MD5Hash\r\nSource Path: SourcePath"
        collector_info_mock.return_value = "Collector: Collector\r\nfilepath: FilePath"
        expected_string = "-- Collection Data     ----------\r\n" \
                          "\r\n" \
                          "*No data collected*\r\n" \
                          "\r\n" \
                          "-- Collection Metadata ----------\r\n" \
                          "Collection Time Stamp: Timestamp\r\n" \
                          "Source MD5: MD5Hash\r\n" \
                          "Source Path: SourcePath\r\n" \
                          "Collector: Collector\r\n" \
                          "filepath: FilePath\r\n" \
                          "---------------------------------\r\n"

        self.assertEqual(expected_string, str(actual_data))


class TestCollectionDataSaveAsMd5(TestCase):
    def test_save_as_md5_bigger_than_4k(self):
        """
        Should store md5 hash 23de9120d4b70ba8cb3f0a980bb6c039 in _sourcehash
        """
        from businesslogic.data import CollectionData

        expected_checksum = "23de9120d4b70ba8cb3f0a980bb6c039"
        with open("./testfiles/longtext.txt") as data:
            expected_data = data.read()
        actual_data = CollectionData(data="")
        actual_data.save_as_md5(expected_data)

        self.assertEqual(expected_checksum, actual_data._sourcehash)


class TestCollectionDataSourcePath(TestCase):
    def test_sourcepath_setter(self):
        """
        Should set _sourcepath and _sourcehash with the MD5 hash of the file provided for _sourcepath
        """
        from businesslogic.data import CollectionData

        expected_hash = "22de9120d4b70ba8cb3f0a980bb6c039"
        if platform.system() == "Windows":
            expected_hash = "69b7d4403901e694c554f8798893e8d9"
        expected_path = "./testfiles/longtext.txt"
        actual_data = CollectionData(data="")
        actual_data.sourcepath = expected_path

        self.assertEqual(expected_path, actual_data._sourcepath)

    def test_sourcepath_does_not_exist(self):
        """
        Should raise FileNotFound error.
        """
        from businesslogic.data import CollectionData

        expected_path = "./testfiles/longtex.txt"
        actual_data = CollectionData(data="")

        with self.assertRaises(FileNotFoundError):
            actual_data.sourcepath = expected_path

    def test_sourcepath_file_zero(self):
        """
        Should set _sourcepath and _sourcehash with the MD5 hash of the file provided for _sourcepath
        """
        from businesslogic.data import CollectionData

        expected_hash = "d41d8cd98f00b204e9800998ecf8427e"
        expected_path = "./testfiles/empty.txt"
        actual_data = CollectionData(data="")
        actual_data.sourcepath = expected_path

        self.assertEqual(expected_hash, actual_data._sourcehash)
        self.assertEqual(expected_path, actual_data._sourcepath)


class TestCollectionMetaDataDunderInit(TestCase):
    def test___init__with_dictionary(self):
        """
        Should use the dictionary a source for the metadata.
        :return:
        """
        expected_metadata = {
            "Metadata1": "Meta_Value_1",
            "Metadata2": "Meta_Value_2"
        }

        actual_metadata = CollectionMetaData(metadata=expected_metadata)

        for expected_key in expected_metadata.keys():
            self.assertEqual(expected_metadata[expected_key], actual_metadata._collectionMetadata[expected_key])

    def test___init__with_empty_dictionary(self):
        """
        Should do nothing.
        :return:
        """
        try:
            CollectionMetaData(metadata={})
        except Exception:
            self.fail()


class TestCollectionMetaDataMetadataFields(TestCase):
    def test_metadata_fields(self):
        """
        Should return generator to iterate over all provided keys provided in __init__
        :return:
        """
        expected_metadata = {
            "Metadata1": "Meta_Value_1",
            "Metadata2": "Meta_Value_2"
        }

        actual_metadata = CollectionMetaData(metadata=expected_metadata)

        for metadata_key in actual_metadata.metadata_fields:
            self.assertEqual(expected_metadata[metadata_key], actual_metadata._collectionMetadata[metadata_key])


class TestCollectionMetaDataGetMetadata(TestCase):
    def test_get_metadata_with_normal_metadata_without_placeholder(self):
        """
        Should return the value for the metadata field.
        :return:
        """
        expected_metadata = {
            "Metadata1": "Meta_Value_1",
            "Metadata2": "Meta_Value_2"
        }
        expected_metadata_key = "Metadata1"

        actual_metadata = CollectionMetaData(metadata=expected_metadata)
        actual_metadata_value = actual_metadata.get_metadata(expected_metadata_key)

        self.assertEqual(expected_metadata[expected_metadata_key], actual_metadata_value)

    def test_get_metadata_with_metadata_with_placeholder(self):
        """
        Should return the metadata value, but the placeholder is replaced with the correct placeholder
        value.
        :return:
        """
        from businesslogic.placeholders import Placeholder

        expected_metadata = {
            "Metadata1": "!@placeholder@!"
        }
        expected_metadata_key = "Metadata1"
        expected_metadata_value = "placeholdervalue"

        Placeholder.update_placeholder(placeholdername="placeholder", placeholdervalue=expected_metadata_value)

        actual_metadata = CollectionMetaData(metadata=expected_metadata)
        actual_metadata_value = actual_metadata.get_metadata(expected_metadata_key)

        self.assertEqual(expected_metadata_value, actual_metadata_value)
