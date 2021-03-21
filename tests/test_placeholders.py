from unittest import TestCase, mock
from unittest.mock import MagicMock

from businesslogic.placeholders import Placeholder


class TestPlaceholder(TestCase):
    @staticmethod
    @mock.patch('os.path', MagicMock(return_value=True))
    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    def test_set_globalplaceholderfile():
        Placeholder.set_globalplaceholderfile('test.txt')

        assert Placeholder._globalplaceholderfile == 'test.txt'
        assert Placeholder._initialize_global_placeholders.called
