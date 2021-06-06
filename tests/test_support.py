from unittest import TestCase

from businesslogic.support import str_to_bool, get_collector_resources, format_bytes


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
        default resources.
        :return: JSON object with the contents of 'collector_text_default.json'
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
        pass

    def test_md5_with_file_longer_than_4k(self):
        pass

    def test_md5_with_file_of_length_zero(self):
        pass

    def test_md5_with_string_shorter_than_4k(self):
        pass

    def test_md5_with_string_of_length_zero(self):
        pass

    def test_md5_with_string_and_with_file(self):
        pass
