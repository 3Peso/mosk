from unittest import TestCase, mock
from unittest.mock import MagicMock


class TestTemperatureFromOpenWeatherDotComDunderInit(TestCase):
    def test___init__(self):
        """
        APIkey should be set after init.
        :return:
        """
        from artefact.network.internet import TemperatureFromOpenWeatherDotCom

        expected_api_key = "hello_api!"
        with mock.patch('artefact.network.internet.TemperatureFromOpenWeatherDotCom._validate_api_key',
                        MagicMock(return_value=True)):
            collector = TemperatureFromOpenWeatherDotCom(parameters={"apikey": expected_api_key}, parent=None)

        actual_api_key = collector.apikey

        self.assertEqual(expected_api_key, actual_api_key)
