"""
mosk source base class module
"""

__version__ = '0.0.1'
__author__ = '3Peso'

import logging
from collections import UserDict

from baseclasses.protocol import ProtocolBase
from businesslogic.placeholders import Placeholder


class SourceBase:
    _logger = logging.getLogger(__name__)

    def __init__(self, parent, parameters, path: str = '', *args, **kwargs):
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
            attributevalue = Placeholder.replace_placeholders(attributes[attributename])
            Placeholder.update_placeholder(attributename, attributevalue)
            SourceBase._logger.debug("Source: Cached source parameter '{}'. Parameter value: '{}'"
                                     .format(attributename, attributevalue))

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, newprotocol: ProtocolBase):
        self._protocol = newprotocol
