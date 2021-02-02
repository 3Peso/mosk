import importlib
from os import path
from xml.dom.minidom import parse, Element, NamedNodeMap
from collections import OrderedDict, UserDict

# installed via pip
# needed for xml schema validation of instructions files
import xmlschema

from businesslogic.log import mosk_logger
from instructionparsers.wrapper import SourceOrArtefactWrapper
from baseclasses.protocol import ProtocolBase
from businesslogic.placeholders import PlaceholderReplacer


class XmlParser:
    PATH_ATTRIBUTE = 'path'
    MODULE_ATTRIBUTE = 'module'
    PLACEHOLDERNAME_ATTRIBUTE = "placeholdername"
    INSTRUCTIONS_ELEMENT = "Instructions"
    XMLSCHEMA_PATH = './instructionparsers/xmlparser.xsd'
    _none_parameter_attributes = frozenset(
        [MODULE_ATTRIBUTE, 'title', PLACEHOLDERNAME_ATTRIBUTE]
    )

    def __init__(self, instructionspath: str, protocol: ProtocolBase):
        self._protocol = protocol
        self._metadata = OrderedDict()
        self.instructionspath = instructionspath

    @property
    def instructionspath(self) -> str:
        """ The getter will return the path to the instructions file provided by the caller.

        The setter will set the new instructions file, if it exists and it will initialize
        the instructions tree in memory. """
        return self._instructionspath

    @instructionspath.setter
    def instructionspath(self, newpath: str):
        if path.isfile(newpath):
            self._validate_schema(newpath)
            self._instructionspath = newpath
            self._sourcesandartefactsTree = self._initializesourcesandartefacts()
            self._initializemetadata()
        else:
            raise FileNotFoundError("'{}' does not exist.".format(newpath))

    @property
    def instructions(self):
        """ Will return the root element of the instructions tree provided in
        the instructions xml file. """
        return self._sourcesandartefactsTree

    @property
    def metadatafields(self):
        return self._metadata.keys()

    @PlaceholderReplacer
    def get_metadata(self, metadatafield):
        return self._metadata[metadatafield]

    @staticmethod
    def _validate_schema(xmlfilepath: str):
        mosk_logger.info("Validating '{}' against xml schema '{}'...".format(xmlfilepath, XmlParser.XMLSCHEMA_PATH))
        schema = xmlschema.XMLSchema(XmlParser.XMLSCHEMA_PATH)
        schema.validate(xmlfilepath)

    def _initializemetadata(self, current: Element = None):
        if current is None:
            current = parse(self._instructionspath).documentElement

        if 'title' in current.attributes:
            # HACK
            # TODO This way of retrieving the text value from the element seems a little bit uncertain in the result
            # depending on how the xml file has been formatted, etc. But for now it works.
            self._metadata[current.attributes['title'].nodeValue] = current.firstChild.nodeValue

        for child in current.childNodes:
            if type(child) is Element:
                self._initializemetadata(child)

    def _initializesourcesandartefacts(self, current: Element = None, soaparent=None,
                                       elementid: int = 0):
        if current is None:
            current = self._get_first_instruction_element()

        currentsoa = getattr(importlib.import_module(current.attributes[XmlParser.MODULE_ATTRIBUTE].nodeValue),
                             current.tagName)(parent=soaparent,
                                              parameters=XmlParser._get_parameter_attributes(current.attributes))
        currentsoa.protocol = self._protocol

        soawrapper = SourceOrArtefactWrapper(element=current, soaelement=currentsoa,
                                             soaparent=soaparent, elementid=elementid,
                                             placeholdername=XmlParser._get_placeholder_name(current))

        for child in current.childNodes:
            if type(child) is Element:
                soawrapper_child = self._initializesourcesandartefacts(current=child, soaparent=currentsoa,
                                                                       elementid=elementid + 1)
                mosk_logger.debug("Adding '{}' with id {} as child of '{}' with id {}.".format(
                    soawrapper_child.element.tagName, soawrapper_child.soawrapperid,
                    soawrapper.element.tagName, soawrapper.soawrapperid
                ))
                soawrapper.addchild(soawrapper_child)
                mosk_logger.debug("Child count of soawrapper with id {} is {}.".format(
                    soawrapper.soawrapperid, len(soawrapper.wrapperchildren)
                ))

        return soawrapper

    def _get_first_instruction_element(self):
        # The first element in the xml branch could be a text element, if there
        # where new lines before the first tag starts.
        nodes = parse(self._instructionspath).getElementsByTagName(XmlParser.INSTRUCTIONS_ELEMENT)[0].childNodes
        # so first we have to get the first REAL xml element
        firstinstructionelement = None
        for node in nodes:
            if type(node) is Element \
                    and node.attributes is not None \
                    and XmlParser.MODULE_ATTRIBUTE in node.attributes.keys():
                firstinstructionelement = node
                break

        return firstinstructionelement

    @staticmethod
    def _get_placeholder_name(current: Element):
        placeholdername = ''
        if XmlParser.PLACEHOLDERNAME_ATTRIBUTE in current.attributes.keys():
            placeholdername = current.attributes[XmlParser.PLACEHOLDERNAME_ATTRIBUTE].nodeValue
        return placeholdername

    @staticmethod
    def _get_parameter_attributes(attributes: NamedNodeMap) -> UserDict:
        parameters = UserDict()
        for parametername in attributes.keys():
            if parametername not in XmlParser._none_parameter_attributes:
                parameters[parametername] = attributes[parametername]

        # parameters = ({parametername: attributes[parametername]} for parametername in attributes.keys()
        # if parametername not in XmlParser._none_parameter_attributes)

        return parameters
