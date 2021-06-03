from unittest import TestCase
from unittest.mock import patch
from xmlschema import XMLSchemaException


class TestXmlParserInstructionspath(TestCase):
    @patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders')
    @patch('instructionparsers.xmlparser.XmlParser._init_instructions')
    @patch('instructionparsers.xmlparser.path.isfile')
    @patch('instructionparsers.xmlparser.XmlParser._validate_schema')
    @patch('instructionparsers.xmlparser.XmlParser._initializemetadata')
    def test_instructionspath(self, placeholder_mock, xmlparser_mock, isfile_mock, schema_mock, initmetadata_mock):
        """
        Will return the instructions file path set in __init__
        """
        from instructionparsers.xmlparser import XmlParser
        expected_file = 'test_instructions.xml'
        isfile_mock.return_value = True
        xml_parser = XmlParser(instructionspath=expected_file, protocol=None)
        actual_file = xml_parser.instructionspath

        self.assertEqual(expected_file, actual_file)

    @patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders')
    @patch('instructionparsers.xmlparser.XmlParser._init_instructions')
    @patch('instructionparsers.xmlparser.path.isfile')
    @patch('instructionparsers.xmlparser.XmlParser._validate_schema')
    @patch('instructionparsers.xmlparser.XmlParser._initializemetadata')
    def test_instructionspath_instruction_file_not_there(self, placeholder_mock, xmlparser_mock, isfile_mock,
                                                         schema_mock, initmetadata_mock):
        """
        Will raise FileNotFound exeption.
        """
        from instructionparsers.xmlparser import XmlParser
        expected_file = 'test_instructions.xml'
        isfile_mock.return_value = True
        xml_parser = XmlParser(instructionspath=expected_file, protocol=None)

        isfile_mock.return_value = False
        with self.assertRaises(FileNotFoundError):
            xml_parser.instructionspath = expected_file


class TestXmlParserValidate_schema(TestCase):
    def test__validate_schema_valid_instructions(self):
        """
        Should do nothing.
        """
        from instructionparsers.xmlparser import XmlParser
        try:
            XmlParser.XMLSCHEMA_PATH = '../instructionparsers/xmlparser.xsd'
            XmlParser._validate_schema(xmlfilepath='./instructions/valid_instructions.xml')
        except XMLSchemaException:
            self.fail("_validate_schema should not raise exception with valid xml instructions.")

    def test__validate_schema_invalid_instructions(self):
        """
        Should raise exception.
        """
        from instructionparsers.xmlparser import XmlParser

        XmlParser.XMLSCHEMA_PATH = '../instructionparsers/xmlparser.xsd'
        self.assertRaises(XMLSchemaException,
                          XmlParser._validate_schema, './instructions/invalid_instructions.xml')

    def test__validate_schema_minimal_valid_instructions(self):
        """
        Should do nothing.
        """
        from instructionparsers.xmlparser import XmlParser
        try:
            XmlParser.XMLSCHEMA_PATH = '../instructionparsers/xmlparser.xsd'
            XmlParser._validate_schema(xmlfilepath='./instructions/minimal_valid_instructions.xml')
        except XMLSchemaException:
            self.fail("_validate_schema should not raise exception with valid xml instructions.")


class TestXmlParserInitializemetadata(TestCase):
    @patch('instructionparsers.xmlparser.XmlParser.instructionspath')
    def test__initializemetadata_valid_instructions(self, path_mock):
        """
        Should initialize member 'metadata' with all elements which have the attribute "title".
        """
        metadata = ('Examiner', 'Assignment', 'Client', 'Description of Artefact', 'Task Description')
        from instructionparsers.xmlparser import XmlParser

        instructions = './instructions/valid_instructions.xml'
        xml_parser = XmlParser(instructionspath=instructions, protocol=None)
        xml_parser._instructionspath = instructions
        xml_parser._initializemetadata()
        for data in metadata:
            with self.subTest(data):
                self.assertIsNotNone(xml_parser.metadata[data])


class TestXmlParserInitInstructions(TestCase):
    @patch('instructionparsers.xmlparser.XmlParser.instructionspath')
    def test__init_instructions_valid_instructions(self, path_mock):
        """
        Should initialize collectors for all XML elements which have the attribute "module".
        """
        from instructionparsers.xmlparser import XmlParser
        from instructionparsers.wrapper import InstructionWrapper

        instructions = './instructions/valid_instructions.xml'
        xml_parser = XmlParser(instructionspath=instructions, protocol=None)

        xml_parser._instructionspath = instructions
        instructionstree = xml_parser._init_instructions()

        self.assertIsInstance(instructionstree, InstructionWrapper)

    @patch('instructionparsers.xmlparser.XmlParser.instructionspath')
    def test__init_instructions_valid_instructions(self, path_mock):
        """
        Should return the instruction tree starting with "Root" node.
        """
        from instructionparsers.xmlparser import XmlParser
        from instructionparsers.wrapper import InstructionWrapper

        instructions = './instructions/valid_instructions.xml'
        xml_parser = XmlParser(instructionspath=instructions, protocol=None)

        xml_parser._instructionspath = instructions
        instructionstree = xml_parser._init_instructions()

        self.assertEqual(instructionstree.instructionname,
                         'Root')
        self.assertEqual(instructionstree.instructionchildren[0].instructionname,
                         'LocalHost')
        self.assertEqual(instructionstree.instructionchildren[0].instructionchildren[0].instructionname,
                         'MachineName')
        self.assertEqual(instructionstree.instructionchildren[1].instructionname, 'LocalHost')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[0].instructionname,
                         'OSName')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[1].instructionname,
                         'OSVersion')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[2].instructionname,
                         'OSTimezone')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[3].instructionname,
                         'AllUsernames')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[4].instructionname,
                         'CurrentUser')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[5].instructionname,
                         'SudoVersion')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[6].instructionname,
                         'FileExistence')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[7].instructionname,
                         'FileExistence')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[8].instructionname,
                         'FileExistence')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[9].instructionname,
                         'FileExistence')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[10].instructionname,
                         'FileExistence')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[11].instructionname,
                         'ShellHistoryOfAllUsers')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[12].instructionname,
                         'NVRAMCollector')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[13].instructionname,
                         'TimeFromNTPServer')
        self.assertEqual(instructionstree.instructionchildren[1].instructionchildren[14].instructionname,
                         'LocalTime')


class TestXmlParserGetFirstInstructionElement(TestCase):
    @patch('instructionparsers.xmlparser.XmlParser.instructionspath')
    def test__get_first_instruction_element(self, path_mock):
        """
        Should return the xml element with the title "Root".
        """
        from instructionparsers.xmlparser import XmlParser
        from xml.dom.minidom import Element
        from instructionparsers.wrapper import InstructionWrapper

        instructions = './instructions/valid_instructions.xml'
        xml_parser = XmlParser(instructionspath=instructions, protocol=None)

        xml_parser._instructionspath = instructions
        element = xml_parser._get_first_instruction_element()

        self.assertIsInstance(element, Element)
        self.assertEqual(element.localName, 'Root')
