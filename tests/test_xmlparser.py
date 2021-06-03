from unittest import TestCase
from unittest.mock import patch
from xmlschema import XMLSchemaException


class TestXmlParser(TestCase):
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

    def test_validate_schema_valid_instructions(self):
        """
        Should do nothing.
        """
        from instructionparsers.xmlparser import XmlParser
        try:
            XmlParser.XMLSCHEMA_PATH = '../instructionparsers/xmlparser.xsd'
            XmlParser._validate_schema(xmlfilepath='./valid_instructions.xml')
        except XMLSchemaException:
            self.fail("_validate_schema should not raise exception with valid xml instructions.")

    def test_validate_schema_invalid_instructions(self):
        """
        Should raise exception.
        """
        from instructionparsers.xmlparser import XmlParser

        XmlParser.XMLSCHEMA_PATH = '../instructionparsers/xmlparser.xsd'
        self.assertRaises(XMLSchemaException,
            XmlParser._validate_schema, './invalid_instructions.xml')
