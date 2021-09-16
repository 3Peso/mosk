"""
mosk network module for classes collecting information from the internet.
"""

__author__ = '3Peso'
__all__ = ['TemperatureFromOpenWeatherDotCom', 'ExternalLinksOnUrl']

import http.client
import json
import logging
import re
from logging import Logger
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from collections import UserDict

from baseclasses.artefact import ArtefactBase


class TemperatureFromOpenWeatherDotCom(ArtefactBase):
    """
    Retrieves the current temperature from OpenWeather.com.

    You need to provide the citiy, country code, and a valid API key, which you can get from
    OpenWeather.com.
    """

    def __init__(self, *args, **kwargs) -> None:
        self._apikey: str = ""
        super().__init__(*args, **kwargs)
        self.__url: str = "https://api.openweathermap.org/data/2.5/weather"
        self.__querytemplate: str = "{}?q={},{}&units=Metric&&APPID={}"

    def _collect(self) -> None:
        try:
            queryurl = self._get_query()
        except AttributeError as attr_err:
            self.data = f"Could not load query. Error: '{str(attr_err)}'."
        else:
            try:
                weather_data = urlopen(queryurl)
            except HTTPError as httperror:
                self.data = f"Could not query {queryurl}.\n{httperror.info}"
            except URLError as urlerr:
                self.data = f"Could not query {queryurl}.\n{str(urlerr)}"
            else:
                if self._weather_data_is_valid(weather_data):
                    data = json.load(weather_data)
                    self.data = f"Current temperature in {self.city}: {data['main']['temp']} °C"
                else:
                    self.data = f"'{queryurl}' returned invalid weather data."

    # REMARKS: Revisit this method. Only checking for the status code is no real help, I think.
    @staticmethod
    def _weather_data_is_valid(weather_data: http.client.HTTPResponse) -> bool:
        logger: Logger = logging.getLogger(__name__)
        if weather_data.getcode() == 200:
            return True
        else:
            logger.warning(f"HTTPResponse code for queryied weather data was '{weather_data.getcode()}'. "
                           f"Status code 200 is a requirement.")
            return False

    def _get_query(self) -> str:
        return self.__querytemplate.format(self.__url, self.city, self.countrycode, self.apikey)

    def _get_parameters_for_str(self) -> UserDict:
        """Overwrite default to prevent logging of API key."""
        filtered: UserDict = {}
        for itemname, itemvalue in self._parameters.items():
            if itemname != 'apikey':
                filtered[itemname] = itemvalue

        return filtered

    @property
    def apikey(self) -> str:
        if self._apikey == "":
            raise AttributeError("apikey not set.")
        else:
            return self._apikey

    @apikey.setter
    def apikey(self, value: str) -> None:
        if self._validate_api_key(value):
            self._apikey = value
        else:
            raise ValueError(f"Provided api key '{value}' does not match the valid format.")

    @staticmethod
    def _validate_api_key(apikey) -> bool:
        valid_apikey_expression = re.compile('^[a-z0-9]{32}$')
        return valid_apikey_expression.match(apikey)


class ExternalLinksOnUrl(ArtefactBase):
    """
    Retrieves all the external links from a provided URL, using BeautifulSoup.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        result: str = ''

        if type(self.data[0].collecteddata) is list:
            for item in self.data[0].collecteddata:
                result += f"{item}\r\n"
        else:
            result += self.data[0].collecteddata
        result += self.data[0].get_metadata_as_str()

        return result

    def _collect(self) -> None:
        self.data = ExternalLinksOnUrl._getexternallinks(self.url)

    @staticmethod
    def _getexternallinks(excludeurl: str) -> list:
        try:
            html = urlopen(excludeurl)
        except URLError as urlerror:
            return f"Cannot open url '{excludeurl}'.\n{urlerror.reason}"
        except HTTPError as httperror:
            return f"Cannot request page '{excludeurl}\n{httperror.reason}'"
        else:
            bs = BeautifulSoup(html, "html.parser")
            parsed_url = urlparse(excludeurl)
            tmp = f"^(http|https)://((?!'+{parsed_url.netloc}+').)*$"
            externallinks = [link['href'] for link in bs.find_all('a', href=re.compile(tmp))
                             if link['href'] is not None]
            return externallinks
