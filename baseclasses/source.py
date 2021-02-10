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
                hasattr(subclass, 'cache__parameters') and
                callable(subclass.cache__parameters))

    def __init__(self, *args, **kwargs):
        return


class SourceBase(Source):
    def __init__(self, parent, parameters, path: str = '', *args, **kwargs):
        Source.__init__(self, *args, **kwargs)
        self.__parent = parent
        self.__path = path
        self.__parameters = parameters
        self.__protocol = None
        SourceBase.cache__parameters(self.__parameters)

    # get__path currently has the soule purpose to document the complete path
    # of an artefact.
    def getpath(self) -> str:
        path = None
        if self.__path is None or self.__path == '':
            path = self.__path

        if path is None and self.__parent is not None:
            path = self.__parent.get__path()
        elif path is None and self.__parent is None:
            raise Exception("__path and __parent cannot be None at the same time.")

        return path

    def getparameter(self, parametername: str):
        return self.__parameters[parametername]

    @classmethod
    def cache__parameters(cls, attributes: UserDict):
        for attributename in attributes.keys():
            attributevalue = PlaceholderReplacer.replace_placeholders(attributes[attributename].nodeValue)
            PlaceholderReplacer.update_placeholder(attributename, attributevalue)
            mosk_logger.debug("Source: Cached source parameter '{}'. Parameter value: '{}'".format(attributename,
                                                                                                   attributevalue))

    @property
    def protocol(self):
        return self.__protocol

    @protocol.setter
    def protocol(self, newprotocol: ProtocolBase):
        self.__protocol = newprotocol
