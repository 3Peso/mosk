from pwd import getpwall

from baseclasses.artefact import ArtefactBase


# TODO Implement switch to collect only users with a folder in '/users/*'
class AllUsernames(ArtefactBase):
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'AllUsernames'
        self.__collectionmethod = 'pwd.getpwall'
        self.__description = 'Collects all usernames with the Python module pwd.'
        # TODO Refactor so that there is no tie to xml (nodeValue) and that the xml attribute values are stored
        # inside the parameters variable
        self.__properties = [item for item in kwargs['parameters']['properties'].nodeValue.split(',')]

    # TODO Refactor
    def __str__(self):
        result = ''
        for item in self._collecteddata:
            itemasstring = ''
            for prop in item:
                itemasstring += "{}\r\n".format(prop)
            result += "{}\r\n".format(itemasstring)

        # Test Commit
        return result

    def collect(self):
        result = []
        for pw in getpwall():
            result.append(["{}: {}".format(prop, getattr(pw, prop)) for prop in self.__properties])
        self._collecteddata = result

    def gettitle(self) -> str:
        return self.__title

    def getcollectionmethod(self) -> str:
        return self.__collectionmethod

    def getdescription(self) -> str:
        return self.__description
