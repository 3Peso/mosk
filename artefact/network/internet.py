import json
import re
from urllib.request import urlopen
from urllib.error import HTTPError
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
        city = self._parameters[self.CITY_PARAMETER].nodeValue
        countrycode = self._parameters[self.COUNTRY_PARAMETER].nodeValue
        apikey = self._parameters[self.API_KEY_PARAMETER].nodeValue
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
