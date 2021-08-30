from unittest import TestCase, mock
from unittest.mock import MagicMock

from artefact.network.internet import TemperatureFromOpenWeatherDotCom

class TestTemperatureFromOpenWeatherDotComDunderInit(TestCase):
    def test___init__(self):
        """
        Should initialize self.__url and self.__querytemplate.
        :return:
        """
        expected_querytemplate = "{}?q={},{}&units=Metric&&APPID={}"
        expected_url = "https://api.openweathermap.org/data/2.5/weather"
        collector = TemperatureFromOpenWeatherDotCom(parameters={}, parent=None)

        self.assertEqual(expected_url, collector._TemperatureFromOpenWeatherDotCom__url)
        self.assertEqual(expected_querytemplate, collector._TemperatureFromOpenWeatherDotCom__querytemplate)


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
            'countrycode': 'ger', 'apikey': '123456789abcdefghijkl1234567890a', 'city': 'Munich'}, parent=None)

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
        excpeted_data = \
            "'https://api.openweathermap.org/data/2.5/weather?q=Munich,ger" \
            "&units=Metric&&APPID=123456789abcdefghijkl1234567890a' " \
                        "returned invalid weather data."
        collector = TemperatureFromOpenWeatherDotCom(parameters={
            'countrycode': 'ger', 'apikey': '123456789abcdefghijkl1234567890a', 'city': 'Munich'}, parent=None)
        collector._apikey = '123456789abcdefghijkl1234567890a'

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
            'countrycode': 'ger', 'apikey': '123456789abcdefghijkl1234567890a'}, parent=None)

        collector._collect()

        self.assertEqual(excpeted_data, collector.data[0].collecteddata)


class TestTemperatureFromOpenWeatherDotComGetParametersForStr(TestCase):
    def test__get_parameters_for_str(self):
        """
        Should get all parameters necessary and store them for logging except the API key.
        :return:
        """
        collector = TemperatureFromOpenWeatherDotCom(parameters={'city': 'Munich',
            'countrycode': 'ger', 'apikey': '123456789abcdefghijkl1234567890a'}, parent=None)

        actual_parameters = collector._get_parameters_for_str()

        self.assertFalse('apikey' in actual_parameters)

class TestTemperatureFromOpenWeatherDotComGetQuery(TestCase):
    def test__get_query(self):
        """
        Should return the initialized query string used to query the weather from openweather.com
        :return:
        """
        expected_query = "https://api.openweathermap.org/data/2.5/weather?q=Munich,ger&units=Metric&&APPID=123456789abcdefghijkl1234567890a"
        collector = TemperatureFromOpenWeatherDotCom(parameters={
            'city': 'Munich', 'countrycode': 'ger', 'apikey': '123456789abcdefghijkl1234567890a'}, parent=None)
        collector._apikey = '123456789abcdefghijkl1234567890a'

        actual_query = collector._get_query()

        self.assertEqual(expected_query, actual_query)

    def test__get_query_missing_city(self):
        """
        Should raise an exception.
        :return:
        """
        collector = TemperatureFromOpenWeatherDotCom(parameters={'countrycode': 'ger', 'apikey':
            '123456789abcdefghijkl1234567890a'},
                                                     parent=None)

        self.assertRaises(AttributeError, collector._get_query)

    def test__get_query_missing_countrycode(self):
        """
        Should raise an exception.
        :return:
        """
        collector = TemperatureFromOpenWeatherDotCom(parameters={'city': 'Munich', 'apikey':
            '123456789abcdefghijkl1234567890a'},
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
        collector = TemperatureFromOpenWeatherDotCom(parameters={
            'countrycode': 'ger', 'apikey': '123456789abcdefghijkl1234567890a', 'city': 'Munich'}, parent=None)

        class FunkyHTTPResponseMockup():
            @staticmethod
            def getcode():
                return 200

        actual_data = FunkyHTTPResponseMockup()

        actual_result = collector._weather_data_is_valid(actual_data)

        self.assertTrue(actual_result)

    def test__weahter_data_is_valid_data_is_invalid(self):
        """
        Should return False
        :return:
        """
        collector = TemperatureFromOpenWeatherDotCom(parameters={
            'countrycode': 'ger', 'apikey': '123456789abcdefghijkl1234567890a', 'city': 'Munich'}, parent=None)

        class FunkyHTTPResponseMockup():
            @staticmethod
            def getcode():
                return 401

        actual_data = FunkyHTTPResponseMockup()

        actual_result = collector._weather_data_is_valid(actual_data)

        self.assertFalse(actual_result)


class TestTemperatureFromOpenWeatherDotComApiKey(TestCase):
    def test_apikey_getter_not_initialized(self):
        """
        Should raise an exception.
        :return:
        """
        collector = TemperatureFromOpenWeatherDotCom(parent=None, parameters={})

        with self.assertRaises(AttributeError):
            tmp = collector.apikey

    def test_apikey_getter(self):
        """
        Should return the value of _apikey
        :return:
        """
        expected_apikey = "12345"
        collector = TemperatureFromOpenWeatherDotCom(parent=None, parameters={})
        collector._apikey = "12345"

        actual_apikey = collector.apikey

        self.assertEqual(expected_apikey, actual_apikey)

    def test_apikey_setter_invalid_format(self):
        """
        Should raise an error.
        :return:
        """
        collector = TemperatureFromOpenWeatherDotCom(parent=None, parameters={})

        with self.assertRaises(ValueError):
            collector.apikey = '12345'

    def test_apikey_setter(self):
        """
        Should set the value of _apikey
        :return:
        """
        expected_key = '123456789abcdefghijkl1234567890a'
        collector = TemperatureFromOpenWeatherDotCom(parent=None, parameters={})
        collector.apikey = expected_key

        self.assertEqual(expected_key, collector._apikey)
