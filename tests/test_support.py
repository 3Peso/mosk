from unittest import TestCase, mock
from unittest.mock import MagicMock
import os
import platform

from businesslogic.support import str_to_bool, get_collector_resources, format_bytes, md5


class TestSupportStrToBool(TestCase):
    def test_str_to_bool_True(self):
        self.assertEqual(str_to_bool('True'), True)

    def test_str_to_bool_False(self):
        self.assertEqual(str_to_bool('False'), False)

    def test_str_to_bool_Empty(self):
        self.assertEqual(str_to_bool(''), False)

    def test_str_to_bool_None(self):
        self.assertEqual(str_to_bool(None), False)

    def test_str_to_bool_any(self):
        self.assertEqual(str_to_bool('Any String'), True)

    def test_str_to_bool_no_str_input_raises_TypeError(self):
        with self.assertRaises(TypeError):
            str_to_bool(23)


class TestGetCollectorResources(TestCase):
    def test_get_collector_resources_no_resources(self):
        """
        When there are no resources files available for current locale it should return the
        default resources. This is also true, if the resource file is there but it is empty.
        :return: JSON object with the contents of 'collector_text_None.json'
        """
        actual_resources = get_collector_resources()

        self.assertIsNotNone(actual_resources)

    def test_get_collector_resources_no_resources_folder(self):
        """
        When there is no local resources folder there should happen nothing (except a logging error
        message been print).
        :return:
        """
        actual_resources = get_collector_resources("./IDoNotExsit")

        self.assertIsNone(actual_resources)

    def test__get_resources_path(self):
        """
        Should return a merged absolute file path when providing a relative path.
        :return:
        """
        from businesslogic.support import _get_resources_path
        expected_path = os.path.abspath('../resources/collector_text_de_DE.json')
        actual_path = _get_resources_path('./resources', 'de_DE')

        self.assertEqual(actual_path, expected_path)

    def test__get_resources_path_countrycode_empty(self):
        """
        Should throw an exception if countrycode is empty.
        :return:
        """
        from businesslogic.support import _get_resources_path
        from businesslogic.errors import NoCountryCodeError

        self.assertRaises(NoCountryCodeError, _get_resources_path, '.', '')

    def test__get_resources_path_resourcepath_empty(self):
        """
        Should throw an exception if resource path is empty.
        :return:
        """
        from businesslogic.support import _get_resources_path
        from businesslogic.errors import NoStringResourcesError

        self.assertRaises(NoStringResourcesError, _get_resources_path, '', 'de_DE')

    def test__load_resources_resourcefilepath_empty(self):
        """
        Should throw an exception, if the resources file path is empty.
        :return:
        """
        from businesslogic.support import _load_resources
        from businesslogic.errors import NoStringResourcesError

        self.assertRaises(NoStringResourcesError, _load_resources, '', 'de_DE')

    def test__load_resources_resourcefilepath_does_not_exist(self):
        """
        Should return None.
        :return:
        """
        from businesslogic.support import _load_resources

        self.assertIsNone(_load_resources('../me_not_exist', 'de_DE'))

    def test__load_resources(self):
        """
        Should return dict object
        :return:
        """
        from businesslogic.support import _load_resources
        resourcesfilepath = os.path.abspath('../resources/collector_text_None.json')
        actual_json_object = _load_resources(resourcesfilepath, 'None')

        self.assertIsInstance(actual_json_object, dict)


class TestFormatBytes(TestCase):
    def test_format_bytes_Kilo(self):
        """Should return 1KB"""
        size = 1025
        expected = "1.0KB"

        self.assertEqual(expected, format_bytes(size))

    def test_format_bytes_Mega(self):
        """Should return 1MB"""
        size = 1048576
        expected = "1.0MB"

        self.assertEqual(expected, format_bytes(size))

    def test_format_bytes_Mega_2(self):
        """Should return 1MB"""
        size = 1048577
        expected = "1.0MB"

        self.assertEqual(expected, format_bytes(size))

    def test_format_bytes_Giga(self):
        """Should return 1GB"""
        size = 1073741824
        expected = "1.0GB"

        self.assertEqual(expected, format_bytes(size))

    def test_format_bytes_Terra(self):
        """Should return 1TB"""
        size = 1099511627776
        expected = "1.0TB"

        self.assertEqual(expected, format_bytes(size))

    def test_format_bytes_Terra_2(self):
        """Should return 1TB"""
        size = 1125899906842624
        expected = "1024.0TB"

        self.assertEqual(expected, format_bytes(size))


class TestMd5(TestCase):
    def test_md5_with_file_shorter_than_4k(self):
        """
        Should return hash 0db7d1adf349b912f612c9be06278706
        """
        expected_hash = "0db7d1adf349b912f612c9be06278706"
        if platform.system() == "Windows":
            expected_hash = "eb9741896e5a38b773be6da56fe90c3a"
        actual_hash = md5(fpath="./testfiles/test.txt")

        self.assertEqual(expected_hash, actual_hash)

    def test_md5_with_file_longer_than_4k(self):
        """
        Should return hash 23de9120d4b70ba8cb3f0a980bb6c039
        """
        expected_hash = "23de9120d4b70ba8cb3f0a980bb6c039"
        if platform.system() == "Windows":
            expected_hash = "69b7d4403901e694c554f8798893e8d9"
        actual_hash = md5(fpath="./testfiles/longtext.txt")

        self.assertEqual(expected_hash, actual_hash)

    def test_md5_with_file_of_length_zero(self):
        """
        Should return hash d41d8cd98f00b204e9800998ecf8427e
        """
        expected_hash = "d41d8cd98f00b204e9800998ecf8427e"
        actual_hash = md5(fpath="./testfiles/empty.txt")

        self.assertEqual(expected_hash, actual_hash)

    def test_md5_with_string_shorter_than_4k(self):
        """
        Should return hash eb733a00c0c9d336e65691a37ab54293
        """
        expected_hash = "eb733a00c0c9d336e65691a37ab54293"
        actual_hash = md5(data="test data")

        self.assertEqual(expected_hash, actual_hash)

    def test_md5_with_string_of_length_zero(self):
        """
        Should return hash d41d8cd98f00b204e9800998ecf8427e
        """
        expected_hash = "d41d8cd98f00b204e9800998ecf8427e"
        actual_hash = md5(data="")

        self.assertEqual(expected_hash, actual_hash)

    def test_md5_with_string_and_with_file(self):
        """
        Should raise ValueError.
        """
        from businesslogic.errors import MD5SupportError

        with self.assertRaises(MD5SupportError):
            md5(data="data", fpath="./testfiles/empty.txt")


class TestChangeToModuleRootDunderInit(TestCase):
    def test___init__(self):
        """
        Should store current working directory.
        :return:
        """
        from businesslogic.support import ChangeToModuleRoot

        expected_wd = "test"
        with mock.patch('businesslogic.support.os.getcwd', MagicMock(return_value=expected_wd)):
            wd_context_manager = ChangeToModuleRoot()
            actual_wd = wd_context_manager._original_working_dir

        self.assertEqual(expected_wd, actual_wd)


class TestChangeToModuleRootDunderEnter(TestCase):
    def setUp(self) -> None:
        self._current_wd = os.getcwd()

    def tearDown(self) -> None:
        os.chdir(self._current_wd)

    def test___enter__(self):
        """
        Should change working directory to module root.
        :return:
        """
        from businesslogic.support import ChangeToModuleRoot

        expected_wd = os.path.abspath('..')
        expected_module_dir = os.path.abspath(".")
        with mock.patch('businesslogic.support.os.path.dirname', MagicMock(return_value=expected_module_dir)):
            wd_context_manager = ChangeToModuleRoot()
            wd_context_manager.__enter__()
            actual_wd = os.getcwd()

        self.assertEqual(expected_wd, actual_wd)


class TestChangeToModuleRoot(TestCase):
    def setUp(self) -> None:
        self._current_wd = os.getcwd()

    def tearDown(self) -> None:
        os.chdir(self._current_wd)

    def test_with(self):
        """
        Should change working directory back to original working directory.
        :return:
        """
        from businesslogic.support import ChangeToModuleRoot

        expected_wd = os.path.abspath('.')
        expected_module_dir = os.path.abspath(".")
        with mock.patch('businesslogic.support.os.path.dirname', MagicMock(return_value=expected_module_dir)):
            with ChangeToModuleRoot():
                print("idle")
            actual_wd = os.getcwd()

        self.assertEqual(expected_wd, actual_wd)


class TestValidateFileSignature(TestCase):
    def test_validate_file_signature_provided_file_does_not_exist(self):
        """
        Should return False.
        :return:
        """
        from businesslogic.support import validate_file_signature

        expected_file_path = "./testfiles/longtext.txt"
        actual_result = validate_file_signature(expected_file_path)

        self.assertFalse(actual_result)

    def test_validate_file_signature_empty_signature_file(self):
        """
        Should return False.
        :return:
        """
        from businesslogic.support import validate_file_signature

        expected_file_path = "./testfiles/test_file_with_empty_signature_file.txt"
        actual_result = validate_file_signature(expected_file_path)

        self.assertFalse(actual_result)

    def test_validate_file_signature_sig_file_windows(self):
        """
        Should return True
        :return:
        """
        from businesslogic.support import validate_file_signature

        expected_file_path = "./testfiles/windows-1252_encoding.txt"
        actual_result = validate_file_signature(expected_file_path)

        self.assertTrue(actual_result)

    def test_validate_file_signature_md5_hash_does_not_match(self):
        """
        Should return False.
        :return:
        """
        from businesslogic.support import validate_file_signature

        expected_file_path = "./testfiles/sig_not_match.txt"
        actual_result = validate_file_signature(expected_file_path)

        self.assertFalse(actual_result)

    def test_validate_file_signature_md5_hash_matches(self):
        """
        Should return True.
        :return:
        """
        from businesslogic.support import validate_file_signature

        expected_file_path = "./testfiles/test.txt"
        actual_result = validate_file_signature(expected_file_path)

        self.assertTrue(actual_result)

    def test_validate_file_signature_no_file_extension(self):
        """
        Should return True.
        :return:
        """
        from businesslogic.support import validate_file_signature

        expected_file_path = "./testfiles/test"
        actual_result = validate_file_signature(expected_file_path)

        self.assertTrue(actual_result)