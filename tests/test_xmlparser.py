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

    def test__init_instrcutions_valid_instructions_with_none_module(self):
        """
        Xml elements with no attribute "module" should be ignored.
        """
        #self.fail()
