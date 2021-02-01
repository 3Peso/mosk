from baseclasses.source import SourceBase


class LocalHost(SourceBase):
    def __init__(self, *args, **kwargs):
        SourceBase.__init__(self, *args, **kwargs)
