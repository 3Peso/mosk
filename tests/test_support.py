from unittest import TestCase, mock

from businesslogic.support import str_to_bool, get_collector_resources


class TestSupportStrToBool(TestCase):
    def test_str_to_bool_True(self):
        assert str_to_bool('True')

    def test_str_to_bool_False(self):
        assert not str_to_bool('False')

    def test_str_to_bool_Empty(self):
        assert not str_to_bool('')

    def test_str_to_bool_None(self):
        assert not str_to_bool(None)

    def test_str_to_bool_any(self):
        assert str_to_bool('Any String')

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

        assert actual_resources is not None

    def test_get_collector_resources_no_resources_folder(self):
        """
        When there is no local resources folder there should happen nothing (except a logging error
        message been print).
        :return:
        """
        actual_resources = get_collector_resources("./IDoNotExsit")

        assert actual_resources is None
