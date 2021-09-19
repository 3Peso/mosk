__author__ = '3Peso'
__all__ = ['Root']

from baseclasses.source import SourceBase


class Root(SourceBase):
    def __init__(self, *args, **kwargs):
        SourceBase.__init__(self, *args, **kwargs)
