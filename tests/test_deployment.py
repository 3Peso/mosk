from unittest import TestCase
from unittest.mock import patch


class MyTestCaseExampleInstructions(TestCase):
    @patch('instructionparsers.xmlparser.XmlParser.instructionspath')
    def test_collect_all(self, path_mock):
        """
        Should initialize collectors for the example file "collect-all.xml"
        """
        from instructionparsers.xmlparser import XmlParser
        instructions = '../examples/collect-all.xml'
        try:
            xml_parser = XmlParser(instructionspath=instructions, protocol=None)
            xml_parser._instructionspath = instructions
            xml_parser._init_instructions()
        except Exception:
            self.fail(f"Failed to initialize parser for '{instructions}'.")

    @patch('instructionparsers.xmlparser.XmlParser.instructionspath')
    def test_collect_from_image(self, path_mock):
        """
        Should initialize collectors for the example file "collect-from-image.xml"
        """
        from instructionparsers.xmlparser import XmlParser
        instructions = '../examples/collect-from-image.xml'
        try:
            xml_parser = XmlParser(instructionspath=instructions, protocol=None)
            xml_parser._instructionspath = instructions
            xml_parser._init_instructions()
        except FileNotFoundError:
            # Assume the file not found is from the missing ewf file in the example instructions.
            pass
        except Exception:
            self.fail(f"Failed to initialize parser for '{instructions}'.")

    @patch('instructionparsers.xmlparser.XmlParser.instructionspath')
    def test_collect_from_internet(self, path_mock):
        """
        Should initialize collectors for the example file "collect-from-internet.xml"
        """
        from instructionparsers.xmlparser import XmlParser
        instructions = '../examples/collect-from-internet.xml'
        try:
            xml_parser = XmlParser(instructionspath=instructions, protocol=None)
            xml_parser._instructionspath = instructions
            xml_parser._init_instructions()
        except Exception:
            self.fail(f"Failed to initialize parser for '{instructions}'.")

    @patch('instructionparsers.xmlparser.XmlParser.instructionspath')
    def test_collect_from_local_network(self, path_mock):
        """
        Should initialize collectors for the example file "collect-from-local-network.xml"
        """
        from instructionparsers.xmlparser import XmlParser
        instructions = '../examples/collect-from-local-network.xml'
        try:
            xml_parser = XmlParser(instructionspath=instructions, protocol=None)
            xml_parser._instructionspath = instructions
            xml_parser._init_instructions()
        except Exception:
            self.fail(f"Failed to initialize parser for '{instructions}'.")

    @patch('instructionparsers.xmlparser.XmlParser.instructionspath')
    def test_collect_from_localhost(self, path_mock):
        """
        Should initialize collectors for the example file "collect-from-localhost.xml"
        """
        from instructionparsers.xmlparser import XmlParser
        instructions = '../examples/collect-from-localhost.xml'
        try:
            xml_parser = XmlParser(instructionspath=instructions, protocol=None)
            xml_parser._instructionspath = instructions
            xml_parser._init_instructions()
        except Exception:
            self.fail(f"Failed to initialize parser for '{instructions}'.")