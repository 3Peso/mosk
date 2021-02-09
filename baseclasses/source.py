from collections import UserDict
from abc import ABCMeta

from baseclasses.protocol import ProtocolBase
from businesslogic.placeholders import PlaceholderReplacer
from businesslogic.log import mosk_logger


class Source(metaclass=ABCMeta):
    @classmethod
    def __subclasshook(cls, subclass):
        return (hasattr(subclass, 'getpath') and
                callable(subclass.getpath) and
                hasattr(subclass, 'getparameter') and
                callable(subclass.getparameter) and
                hasattr(subclass, 'protocol') and
                callable(subclass.protocol) and
                hasattr(subclass, 'cache_parameters') and
                callable(subclass.cache_parameters))

    def __init__(self, *args, **kwargs):
        return


class SourceBase(Source):
    def __init__(self, parent, parameters, path: str = '', *args, **kwargs):
        Source.__init__(self, *args, **kwargs)
        self._parent = parent
        self._path = path
        self._parameters = parameters
        self._protocol = None
        SourceBase.cache_parameters(self._parameters)

    # get_path currently has the soule purpose to document the complete path
    # of an artefact.
    def getpath(self) -> str:
        path = None
        if self._path is None or self._path == '':
            path = self._path

        if path is None and self._parent is not None:
            path = self._parent.get_path()
        elif path is None and self._parent is None:
            raise Exception("_path and _parent cannot be None at the same time.")

        return path

    def getparameter(self, parametername: str):
        return self._parameters[parametername]

    @classmethod
    def cache_parameters(cls, attributes: UserDict):
        for attributename in attributes.keys():
            attributevalue = PlaceholderReplacer.replace_placeholders(attributes[attributename].nodeValue)
            PlaceholderReplacer.update_placeholder(attributename, attributevalue)
            mosk_logger.debug("Source: Cached source parameter '{}'. Parameter value: '{}'".format(attributename,
                                                                                                   attributevalue))

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, newprotocol: ProtocolBase):
        self._protocol = newprotocol
