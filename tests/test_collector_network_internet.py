from unittest import TestCase


class TestTemperatureFromOpenWeatherDotComDunderInit(TestCase):
    def test___init__(self):
        """
        Should initialize self.__url and self.__querytemplate.
        :return:
        """
        self.fail()


class TestTemperatureFromOpenWeatherDotComCollect(TestCase):
    def test__collect(self):
        """
        Should collect the current temperature of the provided city in °C as data from
        openweathermap.org
        :return:
        """
        self.fail()

    def test__collect_openweathermap_not_reachable(self):
        """
        Should log unreachability in the "collected" data as string.
        :return:
        """
        self.fail()

    def test__collect_openweathermap_returns_invalid_json(self):
        """
        Should log invalid state of json in "collected" data as string.
        :return:
        """
        self.fail()

    def test__collect_missing_query_parameter(self):
        """
        Should log the missing parameter(s) in data.
        :return:
        """
        self.fail()


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
        self. fail()

    def test__get_query_missing_parameter(self):
        """
        Should raise an exception.
        :return:
        """