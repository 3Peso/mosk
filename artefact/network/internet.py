import json
import re
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

from baseclasses.artefact import ArtefactBase


class TemperatureFromOpenWeatherDotCom(ArtefactBase):
    CITY_PARAMETER = 'city'
    COUNTRY_PARAMETER = 'countrycode'
    API_KEY_PARAMETER = 'apikey'

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'Current temperature from openweather.com'
        self.__collectionmethod = 'Get data from returend json object.'
        self.__description = 'Calling the API of the webside with free developer api key.'
        self.__url = "https://api.openweathermap.org/data/2.5/weather"
        self.__querytemplate = "{}?q={},{}&units=Metric&&APPID={}"

    def collect(self):
        city = self._parameters[TemperatureFromOpenWeatherDotCom.CITY_PARAMETER].nodeValue
        countrycode = self._parameters[TemperatureFromOpenWeatherDotCom.COUNTRY_PARAMETER].nodeValue
        apikey = self._parameters[TemperatureFromOpenWeatherDotCom.API_KEY_PARAMETER].nodeValue
        queryurl = self._get_query(city, countrycode, apikey)

        try:
            html = urlopen(queryurl)
        except HTTPError as httperror:
            self._collecteddata = "Could not query {}.\n{}".format(queryurl, httperror.info)
        else:
            data = json.load(html)
            self._collecteddata = "Current temperature in {}: {}{}".format(city, data['main']['temp'], '°')

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description

    def _get_query(self, city, countrycode, apikey):
        return self.__querytemplate.format(self.__url, city, countrycode, apikey)


class ExternalLinksOnUrl(ArtefactBase):
    PAGE_URL_PARAMETER = 'url'

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'External Links on Web Page'
        self.__collectionmethod = 'Web Scrapping'
        self.__description = 'Scraps all external urls on a given web page with BeautifulSoup.'

    def __str__(self):
        result = ''

        if type(self._collecteddata) is list:
            for item in self._collecteddata:
                result += "{}\r\n".format(item)
        else:
            result = self._collecteddata

        return result

    def collect(self):
        self._collecteddata = ExternalLinksOnUrl._getexternallinks(self._parameters[
                                                                       ExternalLinksOnUrl.PAGE_URL_PARAMETER].nodeValue)

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description

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
