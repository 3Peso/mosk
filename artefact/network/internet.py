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
    CITY_PARAMETER = 'city'
    COUNTRY_PARAMETER = 'countrycode'
    API_KEY_PARAMETER = 'apikey'

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'Current temperature from openweather.com'
        self._collectionmethod = 'Get data from returend json object.'
        self._description = 'Calling the API of the webside with free developer api key.'
        self.__url = "https://api.openweathermap.org/data/2.5/weather"
        self.__querytemplate = "{}?q={},{}&units=Metric&&APPID={}"

    def collect(self):
        city = self.get_parameter(TemperatureFromOpenWeatherDotCom.CITY_PARAMETER)
        countrycode = self.get_parameter(TemperatureFromOpenWeatherDotCom.COUNTRY_PARAMETER)
        apikey = self.get_parameter(TemperatureFromOpenWeatherDotCom.API_KEY_PARAMETER)
        queryurl = self._get_query(city, countrycode, apikey)

        try:
            html = urlopen(queryurl)
        except HTTPError as httperror:
            self.data = "Could not query {}.\n{}".format(queryurl, httperror.info)
        else:
            data = json.load(html)
        self.data = "Current temperature in {}: {}{}".format(city, data['main']['temp'], '°')

    def _get_query(self, city, countrycode, apikey):
        return self.__querytemplate.format(self.__url, city, countrycode, apikey)


class ExternalLinksOnUrl(ArtefactBase):
    """
    Retrieves all the external links from a provided URL, using BeautifulSoup.
    """
    PAGE_URL_PARAMETER = 'url'

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'External Links on Web Page'
        self._collectionmethod = 'Web Scrapping'
        self._description = 'Scraps all external urls on a given web page with BeautifulSoup.'

    def __str__(self):
        result = ''

        if type(self.data.collecteddata) is list:
            for item in self.data.collecteddata:
                result += "{}\r\n".format(item)
        else:
            result += self.data.collecteddata
        result = self.data.get_metadata_as_str(result)

        return result

    def collect(self):
        self.data = ExternalLinksOnUrl._getexternallinks(self._parameters[ExternalLinksOnUrl.PAGE_URL_PARAMETER])

    @staticmethod
    def _getexternallinks(excludeurl):
        try:
            html = urlopen(excludeurl)
        except URLError as urlerror:
            return "Cannot open url '{}'.\n{}".format(excludeurl, urlerror.reason)
        except HTTPError as httperror:
            return "Cannot request page '{}\n{}'".format(excludeurl, httperror.reason)
        else:
            bs = BeautifulSoup(html, "html.parser")
            # TODO The filtering regex does not exclude internal links as I would like it. Must be sharpened
            externallinks = [link['href'] for link in bs.find_all('a', href=re.compile(
                '^(http|www)((?!'+excludeurl+').)*$'))
                             if link['href'] is not None]
            return externallinks
