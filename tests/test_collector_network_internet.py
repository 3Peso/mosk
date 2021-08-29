from unittest import TestCase, mock
from unittest.mock import MagicMock

from artefact.network.internet import TemperatureFromOpenWeatherDotCom

class TestTemperatureFromOpenWeatherDotComDunderInit(TestCase):
    def test___init__(self):
        """
        Should initialize self.__url and self.__querytemplate.
        :return:
        """
        self.fail()


class TestTemperatureFromOpenWeatherDotComCollect(TestCase):
    @mock.patch('artefact.network.internet.TemperatureFromOpenWeatherDotCom._get_query',
                MagicMock(return_value='http://plumbumm.ich.bin.nicht.da.haha'))
    def test__collect_openweathermap_not_reachable(self):
        """
        Should log unreachability in the "collected" data as string.
        :return:
        """
        excpeted_data = "Could not query http://plumbumm.ich.bin.nicht.da.haha." \
                        "\n<urlopen error [Errno 8] nodename nor servname provided, or not known>"
        collector = TemperatureFromOpenWeatherDotCom(parameters={
            'countrycode': 'ger', 'apikey': '12345', 'city': 'Munich'}, parent=None)

        collector._collect()

        self.assertEqual(excpeted_data, collector.data[0].collecteddata)

    @mock.patch('artefact.network.internet.urlopen',
                MagicMock(return_value='I am invalid'))
    @mock.patch('artefact.network.internet.TemperatureFromOpenWeatherDotCom._weather_data_is_valid',
                MagicMock(return_value=False))
    def test__collect_openweathermap_returns_invalid_json(self):
        """
        Should log invalid state of json in "collected" data as string.
        :return:
        """
        excpeted_data = "'https://api.openweathermap.org/data/2.5/weather?q=Munich,ger&units=Metric&&APPID=12345' " \
                        "returned invalid weather data."
        collector = TemperatureFromOpenWeatherDotCom(parameters={
            'countrycode': 'ger', 'apikey': '12345', 'city': 'Munich'}, parent=None)

        collector._collect()

        self.assertEqual(excpeted_data, collector.data[0].collecteddata)

    def test__collect_missing_query_parameter(self):
        """
        Should log the missing parameter(s) in data.
        :return:
        """
        excpeted_data = "Could not load query. " \
                        "Error: ''TemperatureFromOpenWeatherDotCom' object has no attribute 'city''."
        collector = TemperatureFromOpenWeatherDotCom(parameters={
            'countrycode': 'ger', 'apikey': '12345'}, parent=None)

        collector._collect()

        self.assertEqual(excpeted_data, collector.data[0].collecteddata)


class TestTemperatureFromOpenWeatherDotComGetParametersForStr(TestCase):
    def test__get_parameters_for_str(self):
        """
        Should get all parameters necessary and store them for logging except the API key.
        :return:
        """
        self.fail()


class TestTemperatureFromOpenWeatherDotComGetQuery(TestCase):
    def test__get_query(self):
        """
        Should return the initialized query string used to query the weather from openweather.com
        :return:
        """
        expected_query = "https://api.openweathermap.org/data/2.5/weather?q=Munich,ger&units=Metric&&APPID=12345"
        collector = TemperatureFromOpenWeatherDotCom(parameters={
            'city': 'Munich', 'countrycode': 'ger', 'apikey': '12345'}, parent=None)

        actual_query = collector._get_query()

        self.assertEqual(expected_query, actual_query)

    def test__get_query_missing_city(self):
        """
        Should raise an exception.
        :return:
        """
        collector = TemperatureFromOpenWeatherDotCom(parameters={'countrycode': 'ger', 'apikey': '12345'},
                                                     parent=None)

        self.assertRaises(AttributeError, collector._get_query)

    def test__get_query_missing_countrycode(self):
        """
        Should raise an exception.
        :return:
        """
        collector = TemperatureFromOpenWeatherDotCom(parameters={'city': 'Munich', 'apikey': '12345'},
                                                     parent=None)

        self.assertRaises(AttributeError, collector._get_query)

    def test__get_query_missing_apikey(self):
        """
        Should raise an exception.
        :return:
        """
        collector = TemperatureFromOpenWeatherDotCom(parameters={'city': 'Munich', 'countrycode': 'ger'},
                                                     parent=None)

        self.assertRaises(AttributeError, collector._get_query)

class TestTemperatureFromOpenWeatherDotComWeatherDataIsValid(TestCase):
    def test__weather_data_is_valid(self):
        """
        Should return True
        :return:
        """
        self.fail()

    def test__weahter_data_is_valid_data_is_invalid(self):
        """
        Should return False
        :return:
        """
        self.fail()