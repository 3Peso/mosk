__author__ = '3Peso'
__all__ = ['Network']

from baseclasses.source import SourceBase


class Network(SourceBase):
    def __init__(self, *args, **kwargs):
        SourceBase.__init__(self, *args, **kwargs)