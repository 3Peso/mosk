"""
mosk network module for classes collecting information from the internet.
"""

__author__ = '3Peso'
__all__ = ['TemperatureFromOpenWeatherDotCom', 'ExternalLinksOnUrl']

import json
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

from baseclasses.artefact import ArtefactBase


class TemperatureFromOpenWeatherDotCom(ArtefactBase):
    """
    Retrieves the current temperature from OpenWeather.com.

    You need to provide the citiy, country code, and a valid API key, which you can get from
    OpenWeather.com.
    """

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__url = "https://api.openweathermap.org/data/2.5/weather"
        self.__querytemplate = "{}?q={},{}&units=Metric&&APPID={}"

    def _collect(self):
        queryurl = self._get_query(self.city, self.countrycode, self.apikey)

        try:
            html = urlopen(queryurl)
        except HTTPError as httperror:
            self.data = f"Could not query {queryurl}.\n{httperror.info}"
        else:
            data = json.load(html)
        self.data = f"Current temperature in {self.city}: {data['main']['temp']} °C"

    def _get_query(self):
        return self.__querytemplate.format(self.__url, self.city, self.countrycode, self.apikey)


class ExternalLinksOnUrl(ArtefactBase):
    """
    Retrieves all the external links from a provided URL, using BeautifulSoup.
    """

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)

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
