from unittest import TestCase

from businesslogic.support import str_to_bool, get_collector_resources


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
