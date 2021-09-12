"""mosk artefact base class module"""__author__ = '3Peso'__all__ = ['ArtefactBase', 'MacArtefact']import loggingimport platformfrom datetime import datetimefrom abc import abstractmethodfrom collections import UserDictfrom businesslogic.placeholders import Placeholderfrom businesslogic.data import CollectionDatafrom businesslogic.support import get_collector_resourcesclass ArtefactBase(object):    """    Base class for all artefact collection classes.    """    _logger = logging.getLogger(__name__)    def __init__(self, parent, parameters: dict = None, *args, **kwargs):        self._parent = parent        self._parameters = parameters        self._collecteddata = []        self._protocol = None        self._init_description_properties()        ArtefactBase.cache_parameters(self._parameters)        self._set_parameters_as_attributes(parameters)        self._supportedplatform = []    def getdocumentation(self) -> str:        """        Returns the documentation information of the collector/artefact as string.        :return:        """        try:            # Example            # Title: CurrentUser            # Description: Collects the current user name on the local host.            # Collection Method: getpass.getuser()            documentation = "Title: {}\nDescription: {}\nCollection Method: {}".format(self._title,                                                                                       self._description,                                                                                       self._collectionmethod)        except TypeError:            documentation = ""        return documentation    def __call__(self):        """        Calls the _collect method of the underlying collector. Ensures, that a meaningfull error message is been logged        if an exception occurs during collection runs. Also ensures, that the collector will only start to collect        information, if the underlying platform is supported by the collector.        Do not call the _collect method directly.        :return:        """        logger = logging.getLogger(__name__)        if len(self._supportedplatform) == 0 or platform.system() in self._supportedplatform:            try:                self._collect()            except Exception as unhandled:                message = f"Caught unhandled exception during collection of artefact. Exception: {str(unhandled)}"                logger.error(message)                self.data = message        else:            self.data = f'The platform "{platform.system()}" is not supported by this collector. ' \                        f'\r\nPlatform supported: "{self._supportedplatform}"'    def __str__(self):        """        Converts all collected data objects in _collecteddata into string objects, and returns one string,        containing all information, which is the name of the collector class for each object, and, if any,        the calling parameters and their values of the collector.        :return:        """        if self.data is None:            ArtefactBase._logger.warning(f"ArtefactBase: Collected data of '{self._title}' is None")        else:            ArtefactBase._logger.debug(                f"ArtefactBase: Collected data of '{self._title}' converted to string in ArtefactBase.__str__")            data_as_string = ''            if hasattr(self.data, '__iter__'):                for dataobj in self.data:                    # HACK                    # Adding this collector metadata here is not the best place. Normally this should be                    # done during collection time. But I havn't figured out a place where to put this                    # without the need to change every collector there is. So, as long as the collector                    # metadata is only used in __str__ it can stay here.                    dataobj._collector_name = self.get_subclass_name()                    if len(self._parameters.items()) > 0:                        self._logger.debug(f"Setting collector {len(self._parameters)} parameters for __str__.")                        dataobj.collector_parameters = self._get_parameters_for_str()                    data_as_string += f"{str(dataobj)}\r\n"            else:                data_as_string = str(self.data)        return data_as_string    def _set_parameters_as_attributes(self, parameters: dict = None):        for parameter, value in parameters.items():            setattr(self, parameter, Placeholder.replace_placeholders(value))            parameters[parameter] = Placeholder.replace_placeholders(value)    def _init_description_properties(self):        self._title = None        self._description = None        self._collectionmethod = None        resources = get_collector_resources()        try:            resources = resources[self.get_subclass_name()]            try:                self._title = resources['title']            except KeyError:                self._title = "No Title Found"            try:                self._description = resources['description']            except KeyError:                self._description = "No Description Found"            try:                self._collectionmethod = resources['collectionmethod']            except KeyError:                self._collectionmethod = "No Collection Method Found"        except KeyError:            self._logger.info(f'No resource string for collector "{self.get_subclass_name()}" in resources.')    # From: https://stackoverflow.com/questions/19335722/getting-name-of-subclass-from-superclass    def get_subclass_name(self):        return f"{self.__class__.__module__}.{self.__class__.__name__}"    @classmethod    def cache_parameters(cls, attributes: UserDict = None):        """Cache placeholder values for later usage in following commands."""        for attributename in attributes.keys():            attributevalue = Placeholder.replace_placeholders(attributes[attributename])            Placeholder.update_placeholder(attributename, attributevalue)            ArtefactBase._logger.debug(                f"Artefact: Cached artefact parameter '{attributename}'. Parameter value: '{attributevalue}'")    @abstractmethod    def _collect(self):        pass    def _get_parameters_for_str(self):        return self._parameters    @property    def protocol(self):        return self._protocol    @protocol.setter    # Normally I would define the type of the parameter "newprotocol" as ProtocolBase.    # But baseclasses.protocol already imports baseclasses.artefact. This would create    # a cyclic dependency.    def protocol(self, newprotocol):        self._protocol = newprotocol    @property    def data(self):        """        :return:        List with collected data objects.        """        return self._collecteddata    @data.setter    def data(self, value):        """        Setter to append more collected data to a list with data objects.        :param value: If value is 'None' the list is emptied.        :return:        """        if value is None:            self._collecteddata = []        else:            self._collecteddata.append(CollectionData(data=value, currentdatetime=datetime.now()))    @Placeholder    def get_parameter(self, parameter: str):        parametervalue = self._parameters[parameter]        self._logger.debug(f"Retrieved parameter '{parameter}': '{parametervalue}'")        return parametervalue    def is_platform_supported(self):        return platform.system() in self._supportedplatform    @property    def supported_platform(self):        return self._supportedplatform    @supported_platform.setter    def supported_platform(self, value):        logger = logging.getLogger(__name__)        if value not in self._supportedplatform:            self._supportedplatform.append(value)        else:            logger.info(f"Did not add '{value}' to supported platforms, because it already is in supported platforms.")class MacArtefact(ArtefactBase):    def __init__(self, *args, **kwargs):        super().__init__(*args, **kwargs)        self.supported_platform = 'Darwin'    def _collect(self):        passclass LinuxArtefact(ArtefactBase):    def __init__(self, *args, **kwargs):        super().__init__(*args, **kwargs)        self.supported_platform = 'Linux'    def _collect(self):        pass