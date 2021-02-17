import loggingfrom abc import ABCMeta, abstractmethodfrom collections import UserDictfrom baseclasses.source import Sourcefrom baseclasses.protocol import ProtocolBasefrom businesslogic.placeholders import PlaceholderReplacer# TODO: Maybe I should rethink the use of ABCs here and everywhere else# I try to build my own ones.# TODO: docstring documentation to document the protocol / interfaceclass Artefact(metaclass=ABCMeta):    @classmethod    def __subclasshook__(cls, subclass):        return (hasattr(subclass, 'collect') and                callable(subclass.collect) and                hasattr(subclass, 'getdocumentation') and                callable(subclass.getdocumentation) and                hasattr(subclass, 'gettitle') and                callable(subclass.gettitle) and                hasattr(subclass, 'getcollectionmethod') and                callable(subclass.getcollectionmethod) and                hasattr(subclass, 'getdescription') and                callable(subclass.getdescription) and                hasattr(subclass, 'cache_parameters') and                callable(subclass.cache_parameters))    def __init__(self, *args, **kwargs):        returnclass ArtefactBase(Artefact):    _logger = logging.getLogger(__name__)    def __init__(self, parent: Source, parameters, *args, **kwargs):        Artefact.__init__(self, *args, **kwargs)        self._parent = Source(parent)        self._parameters = dict(parameters)        self._collecteddata = None        self._protocol = None        ArtefactBase.cache_parameters(self._parameters)    def getdocumentation(self) -> str:        # Example        # Title: CurrentUser        # Description: Collects the current user name on the local host.        # Collection Method: getpass.getuser()        documentation = "Title: {}\nDescription: {}\nCollection Method: {}".format(self.gettitle(),                                                                                   self.getdescription(),                                                                                   self.getcollectionmethod())        return documentation    def __call__(self):        return self.collect()    @classmethod    def cache_parameters(cls, attributes: UserDict):        for attributename in attributes.keys():            attributevalue = PlaceholderReplacer.replace_placeholders(attributes[attributename].nodeValue)            PlaceholderReplacer.update_placeholder(attributename, attributevalue)            ArtefactBase._logger.debug("Artefact: Cached artefact parameter '{}'. Parameter value: '{}'".                                       format(attributename, attributevalue))    def __str__(self):        if self.data is None:            ArtefactBase._logger.warn("ArtefactBase: Collected data of '{}' is None".format(self.gettitle()))        else:            ArtefactBase._logger.debug(                "ArtefactBase: Collected data of '{}' converted to string in ArtefactBase.__str__".                format(self.gettitle()))        return self.data    @abstractmethod    def collect(self) -> dict:        pass    @abstractmethod    def gettitle(self) -> str:        pass    @abstractmethod    def getcollectionmethod(self) -> str:        pass    @abstractmethod    def getdescription(self) -> str:        pass    @property    def protocol(self):        return self._protocol    @protocol.setter    def protocol(self, newprotocol: ProtocolBase):        self._protocol = newprotocol    @property    def data(self):        return self._collecteddata