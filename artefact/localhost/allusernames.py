"""
mosk localhost module for classes collecting information about all users.
"""

__version__ = '0.0.1'
__author__ = '3Peso'

from pwd import getpwall

from baseclasses.artefact import ArtefactBase


# TODO Implement switch to collect only users with a folder in '/users/*'
class AllUsernames(ArtefactBase):
    """
    Gets all user names retrievable by python.
    """
    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self._title = 'AllUsernames'
        self._collectionmethod = 'pwd.getpwall'
        self._description = 'Collects all usernames with the Python module pwd.'
        # inside the parameters variable
        self.__properties = [item for item in kwargs['parameters']['properties'].split(',')]

    # TODO Refactor
    def __str__(self):
        result = ''
        for item in self.data.collecteddata:
            itemasstring = ''
            for prop in item:
                itemasstring += "{}\r\n".format(prop)
            result += "{}\r\n".format(itemasstring)
        result = self.data.get_metadata_as_str(result)

        return result

    def collect(self):
        result = []
        for pw in getpwall():
            result.append(["{}: {}".format(prop, getattr(pw, prop)) for prop in self.__properties])
        self.data = result
