from unittest import TestCase

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
        actual_hash = md5(fpath="./testfiles/test.txt")

        self.assertEqual(expected_hash, actual_hash)

    def test_md5_with_file_longer_than_4k(self):
        """
        Should return hash 23de9120d4b70ba8cb3f0a980bb6c039
        """
        expected_hash = "23de9120d4b70ba8cb3f0a980bb6c039"
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
        with self.assertRaises(ValueError):
            md5(data="data", fpath="./testfiles/empty.txt")
