"""
mosk network module for classes collecting information from the internet.
"""

__author__ = '3Peso'
__all__ = ['TemperatureFromOpenWeatherDotCom', 'ExternalLinksOnUrl']

import http.client
import json
import logging
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from collections import UserDict

from baseclasses.artefact import ArtefactBase


class TemperatureFromOpenWeatherDotCom(ArtefactBase):
    """
    Retrieves the current temperature from OpenWeather.com.

    You need to provide the citiy, country code, and a valid API key, which you can get from
    OpenWeather.com.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__url = "https://api.openweathermap.org/data/2.5/weather"
        self.__querytemplate = "{}?q={},{}&units=Metric&&APPID={}"

    def _collect(self):
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

    @staticmethod
    def _weather_data_is_valid(weather_data: http.client.HTTPResponse):
        logger = logging.getLogger(__name__)
        if weather_data.getcode() == 200:
            return True
        else:
            logger.warning(f"HTTPResponse code for queryied weather data was '{weather_data.getcode()}'. "
                           f"Status code 200 is a requirement.")
            return False

    def _get_query(self):
        return self.__querytemplate.format(self.__url, self.city, self.countrycode, self.apikey)

    def _get_parameters_for_str(self):
        """Overwrite default to prevent logging of API key."""
        filtered: UserDict = {}
        for itemname, itemvalue in self._parameters.items():
            if itemname != 'apikey':
                filtered[itemname] = itemvalue

        return filtered

    #@property
    #def apikey(self):
    #    return self._apikey

    #@property.setter
    #def apikey(self, value):
    #    self._apikey = value


class ExternalLinksOnUrl(ArtefactBase):
    """
    Retrieves all the external links from a provided URL, using BeautifulSoup.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        result = ''

        if type(self.data[0].collecteddata) is list:
            for item in self.data[0].collecteddata:
                result += f"{item}\r\n"
        else:
            result += self.data[0].collecteddata
        result = self.data[0].get_metadata_as_str(result)

        return result

    def _collect(self):
        self.data = ExternalLinksOnUrl._getexternallinks(self.url)

    @staticmethod
    def _getexternallinks(excludeurl):
        try:
            html = urlopen(excludeurl)
        except URLError as urlerror:
            return f"Cannot open url '{excludeurl}'.\n{urlerror.reason}"
        except HTTPError as httperror:
            return f"Cannot request page '{excludeurl}\n{httperror.reason}'"
        else:
            bs = BeautifulSoup(html, "html.parser")
            # TODO The filtering regex does not exclude internal links as I would like it. Must be sharpened
            externallinks = [link['href'] for link in bs.find_all('a', href=re.compile(
                '^(http|www)((?!'+excludeurl+').)*$'))
                             if link['href'] is not None]
            return externallinks
