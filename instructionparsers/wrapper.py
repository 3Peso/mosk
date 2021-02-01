from xml.dom.minidom import Element, NamedNodeMap


# TODO Find a better name for that class
class SourceOrArtefactWrapper:
    def __init__(self, element: Element, soaelement, soaparent, elementid: int, placeholdername: str = ''):
        self._element = element
        self._soaelement = soaelement
        self._soaparent = soaparent
        self._elementdata = element.attributes
        self._elementid = elementid
        self._soachildren = []
        self._placeholdername = placeholdername

    def __str__(self):
        return "{}:{}".format(self._element.tagName, self._elementid)

    @property
    def soaelement(self):
        return self._soaelement

    @property
    def elementdata(self):
        return self._elementdata

    @property
    def element(self):
        return self._element

    @property
    def soawrapperid(self):
        return self._elementid

    @property
    def wrapperchildren(self):
        return self._soachildren

    @property
    def placeholdername(self):
        return self._placeholdername

    def addchild(self, child):
        self._soachildren.append(child)

