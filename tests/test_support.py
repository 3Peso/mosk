from unittest import TestCase, mock

from businesslogic.support import str_to_bool


class TestSupport(TestCase):
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