import logging
import platform
from unittest import TestCase, mock
from unittest.mock import MagicMock, patch


class TestArtefactBaseDataSetter(TestCase):
    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    def test_data_setter(self):
        """
        Should add the provided value as data object to its data object list
        :return:
        """
        from baseclasses.artefact import ArtefactBase
        artefact = ArtefactBase(parent=None, parameters={})
        artefact.data = "Some data"

        self.assertEqual(len(artefact.data), 1)

    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    def test_data_setter_with_two_objects(self):
        """
        Should append data to the data object array if there are more data objects to be collected
        :return:
        """
        from baseclasses.artefact import ArtefactBase
        artefact = ArtefactBase(parent=None, parameters={})
        artefact.data = "Some data"
        artefact.data = "More data"

        self.assertEqual(len(artefact.data), 2)

    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    def test_data_setter_overwrite(self):
        """
        Should overwrite existing collected data if None is provided as data object
        :return:
        """
        from baseclasses.artefact import ArtefactBase
        artefact = ArtefactBase(parent=None, parameters={})
        artefact.data = "Some data"
        artefact.data = "More data"

        artefact.data = None

        self.assertEqual(len(artefact.data), 0)


class TestArtefactBaseInitDescription(TestCase):
    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    def test__init_description_properties_with_missing_resources(self):
        """
        Should initialize properties _title, _description, and _collectionmethod with None
        """
        from baseclasses.artefact import ArtefactBase
        artefact = ArtefactBase(parent=None, parameters={})

        self.assertIsNone(artefact._title)
        self.assertIsNone(artefact._description)
        self.assertIsNone(artefact._collectionmethod)

    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    def test__init_description_properties_with_missing_resources_for_collector(self):
        """
        Should initialize properties _title, _description, and _collectionmethod with None,
        if there are no string for the current collector
        """
        from baseclasses.artefact import ArtefactBase
        artefact = ArtefactBase(parent=None, parameters={})

        self.assertIsNone(artefact._title)
        self.assertIsNone(artefact._description)
        self.assertIsNone(artefact._collectionmethod)

    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    def test__init_description_properties(self):
        """
        Should initialize properties _title, _description, and _collectionmethod
        """
        from tests.support.mockups import SimpleArtefactMockup
        artefact = SimpleArtefactMockup(parent=None, parameters={})

        self.assertEqual(artefact._title, 'SimpleArtefactMockup')
        self.assertEqual(artefact._description, 'This is a mockup collector.')
        self.assertEqual(artefact._collectionmethod, 'mockup')


class TestArtefactBaseCacheParameters(TestCase):
    def test_cache_parameters_not_defined(self):
        """
        Should add the new placeholder to the global placeholders dictionary of Placeholders.
        """
        from baseclasses.artefact import ArtefactBase
        from businesslogic.placeholders import Placeholder

        artefact = ArtefactBase(parent=None, parameters={})

        expected_value = "value"
        expected_attribute = "attribute"
        artefact.cache_parameters({expected_attribute: expected_value})

        try:
            actual_value = Placeholder._instruction_placeholders[expected_attribute]
            self.assertEqual(expected_value, actual_value)
        except Exception:
            self.fail()

    def test_cache_parameters_already_defined(self):
        """
        Should overwrite the placeholder in the global placeholders dictionary of Placeholders.
        """
        from baseclasses.artefact import ArtefactBase
        from businesslogic.placeholders import Placeholder

        artefact = ArtefactBase(parent=None, parameters={})

        expected_value = "value"
        expected_attribute = "attribute"
        Placeholder._instruction_placeholders[expected_attribute] = expected_value
        expected_new_value = "new value"
        artefact.cache_parameters({expected_attribute: expected_new_value})

        try:
            actual_value = Placeholder._instruction_placeholders[expected_attribute]
            self.assertEqual(expected_new_value, actual_value)
        except Exception:
            self.fail()


class TestArtefactBaseDunderCall(TestCase):
    def test___call__with_unhandled_exception(self):
        """
        Should log a meaningfull error message in collected data.
        :return:
        """
        from tests.support.mockups import ExceptionArtefactMockup

        expected_message = "Caught unhandled exception during collection of artefact. " \
                           "Exception: There is something wrong with your values."
        actual_artefact = ExceptionArtefactMockup(parent=None, parameters={})
        actual_artefact._supportedplatform = []
        try:
            logging.disable(logging.ERROR)
            # Collect by using __call__
            actual_artefact()
        finally:
            logging.disable(logging.NOTSET)
        actual_message = actual_artefact.data[0].collecteddata

        self.assertEqual(actual_message, expected_message)

    def test___call__with_unsupported_platform(self):
        """
        Should log, that the selected collector is not supported by the underlying plattform.
        :return:
        """
        from tests.support.mockups import ExceptionArtefactMockup

        expected_message = 'The platform "{}" is not supported by this collector. ' \
                           '\r\nPlatform supported: "[\'MamboJamboPlatform\']"'.format(platform.system())
        actual_artefact = ExceptionArtefactMockup(parent=None, parameters={})

        # Collect by using __call__
        actual_artefact()
        actual_message = actual_artefact.data[0].collecteddata

        self.assertEqual(actual_message, expected_message)

    def test___call__with_unsupported_platform_version(self):
        """
        Should log in data, that the platform verion is not supported
        :return:
        """
        from tests.support.mockups import SimpleArtefactMockup

        expected_min_version = "1.0.0.0"
        expected_max_version = "2.0.0.0"
        expected_platform_version = "0.9.0.0"
        expected_message = 'The platform "{}" with its version "{}" is not supported by this collector. ' \
                           '\r\nMinimal version supported: "{}". Max version supported: "{}"' \
            .format(platform.system(), expected_platform_version, expected_min_version, expected_max_version)
        actual_artefact = SimpleArtefactMockup(parent=None, parameters={})
        actual_artefact._platform_version = expected_platform_version
        actual_artefact._min_platform_version = expected_min_version
        actual_artefact._max_platform_version = expected_max_version

        # Collect by using __call__
        with mock.patch('baseclasses.artefact.ArtefactBase.is_platform_version_supported',
                        MagicMock(return_value=False)):
            actual_artefact()

        actual_message = actual_artefact.data[0].collecteddata

        self.assertEqual(actual_message, expected_message)


class TestArtefactBaseDunderStr(TestCase):
    def test___str__data_is_none(self):
        """
        Should return empty string.
        :return:
        """
        from tests.support.mockups import ExceptionArtefactMockup

        expected_string = ''
        actual_artefact = ExceptionArtefactMockup(parent=None, parameters={})

        actual_artefact_as_string = str(actual_artefact)

        self.assertEqual(expected_string, actual_artefact_as_string)


class TestArtefactBaseGetDocumentation(TestCase):
    def test_getdocumentation(self):
        """
        Should return string with the documentation information for that collector.
        :return:
        """
        from tests.support.mockups import ExceptionArtefactMockup

        expected_documentation = 'Title: Title\nDescription: Description\nCollection Method: Method'
        actual_artefact = ExceptionArtefactMockup(parent=None, parameters={})
        actual_artefact._title = "Title"
        actual_artefact._description = "Description"
        actual_artefact._collectionmethod = "Method"

        actual_documentation = actual_artefact.getdocumentation()

        self.assertEqual(actual_documentation, expected_documentation)


class TestArtefactBaseInitDescriptionProperties(TestCase):
    def test__init_description_properties(self):
        """
        Should initialize _title, _description, _collectionmethod, looking these infos up in the resources file
        which is currently in use.
        :return:
        """
        from tests.support.mockups import SimpleArtefactMockup
        expected_resources = {
            'tests.support.mockups.SimpleArtefactMockup': {
                'title': 'Test Title',
                'description': 'Test Description',
                'collectionmethod': 'Method'
            }
        }
        with mock.patch('baseclasses.artefact.get_collector_resources',
                        MagicMock(return_value=expected_resources)):
            actual_artefact = SimpleArtefactMockup(parameters={}, parent={})
            actual_artefact._init_description_properties()

        self.assertEqual(expected_resources['tests.support.mockups.SimpleArtefactMockup']['title'],
                         actual_artefact._title)
        self.assertEqual(expected_resources['tests.support.mockups.SimpleArtefactMockup']['description'],
                         actual_artefact._description)
        self.assertEqual(expected_resources['tests.support.mockups.SimpleArtefactMockup']['collectionmethod'],
                         actual_artefact._collectionmethod)

    def test__init_description_properties_no_title_found(self):
        """
        Should init _title with "No title found".
        :return:
        """
        from tests.support.mockups import SimpleArtefactMockup
        expected_resources = {
            'tests.support.mockups.SimpleArtefactMockup': {
                'description': 'Test Description',
                'collectionmethod': 'Method'
            }
        }
        with mock.patch('baseclasses.artefact.get_collector_resources',
                        MagicMock(return_value=expected_resources)):
            actual_artefact = SimpleArtefactMockup(parameters={}, parent={})
            actual_artefact._init_description_properties()

        self.assertEqual("No Title Found", actual_artefact._title)

    def test__init_description_properties_no_description_found(self):
        """
        Should init _description with "No description found".
        :return:
        """
        from tests.support.mockups import SimpleArtefactMockup
        expected_resources = {
            'tests.support.mockups.SimpleArtefactMockup': {
                'title': 'Title',
                'collectionmethod': 'Method'
            }
        }
        with mock.patch('baseclasses.artefact.get_collector_resources',
                        MagicMock(return_value=expected_resources)):
            actual_artefact = SimpleArtefactMockup(parameters={}, parent={})
            actual_artefact._init_description_properties()

        self.assertEqual("No Description Found", actual_artefact._description)

    def test__init_description_properties_no_colletionmethod_found(self):
        """
        Should init _collectionmethod with "No collection method found".
        :return:
        """
        from tests.support.mockups import SimpleArtefactMockup
        expected_resources = {
            'tests.support.mockups.SimpleArtefactMockup': {
                'title': 'Title',
                'description': 'Description'
            }
        }
        with mock.patch('baseclasses.artefact.get_collector_resources',
                        MagicMock(return_value=expected_resources)):
            actual_artefact = SimpleArtefactMockup(parameters={}, parent={})
            actual_artefact._init_description_properties()

        self.assertEqual("No Collection Method Found", actual_artefact._collectionmethod)


class TestArtefactBaseSupportedPlatform(TestCase):
    def test_supported_platform_set_multiple_platforms(self):
        """
        Should add all platforms to the member list _supportedplatform
        :return:
        """
        from tests.support.mockups import SimpleArtefactMockup

        expected_platforms = "['Platform1', 'Platform2', 'Platform3']"
        collector = SimpleArtefactMockup(parameters={}, parent=None)

        collector.supported_platform = "Platform1"
        collector.supported_platform = "Platform2"
        collector.supported_platform = "Platform3"

        self.assertEqual(expected_platforms, str(collector._supportedplatform))

    def test_supported_platform_set_same_platform_twice(self):
        """
        Should add a supported platform just once.
        :return:
        """
        from tests.support.mockups import SimpleArtefactMockup

        expected_platforms = "['Platform1', 'Platform2']"
        collector = SimpleArtefactMockup(parameters={}, parent=None)

        collector.supported_platform = "Platform1"
        collector.supported_platform = "Platform2"
        collector.supported_platform = "Platform2"

        self.assertEqual(expected_platforms, str(collector._supportedplatform))

    def test_supported_platform_getter(self):
        """
        Should return the memberlist _supportedplatform
        :return:
        """
        from tests.support.mockups import SimpleArtefactMockup

        expected_platforms = "['Platform1', 'Platform2', 'Platform3']"
        collector = SimpleArtefactMockup(parameters={}, parent=None)

        collector.supported_platform = "Platform1"
        collector.supported_platform = "Platform2"
        collector.supported_platform = "Platform3"

        actual_platforms = collector.supported_platform

        self.assertEqual(expected_platforms, str(actual_platforms))


class TestArtefactBase(TestCase):
    def test_is_platform_supported_with_multiple_supported_platforms(self):
        """
        Should return true
        :return:
        """
        from tests.support.mockups import SimpleArtefactMockup

        expected_support = True
        collector = SimpleArtefactMockup(parameters={}, parent=None)

        collector.supported_platform = "Platform1"
        collector.supported_platform = "Platform2"
        collector.supported_platform = "Platform3"

        with mock.patch('baseclasses.artefact.platform.system', MagicMock(return_value='Platform1')):
            actual_support = collector.is_platform_supported()

        self.assertEqual(expected_support, actual_support)


class TestFileClassFilePathProperty(TestCase):
    def test_filepath_setter_with_trailing_whitespace_chars(self):
        """
        Should remove whitespace chars like '\r' and '\n'
        :return:
        """
        from baseclasses.artefact import FileClass

        expected_file_path = "./somepath"
        fileobj = FileClass()

        fileobj.source_path = './somepath\r\n'
        actual_file_path = fileobj.source_path

        self.assertEqual(expected_file_path, actual_file_path)

    def test_filepath_setter_with_home_abbreviation(self):
        """
        Should expand the file path.
        :return:
        """
        from baseclasses.artefact import FileClass

        expected_file_path = "/home/testuser/somepath"
        fileobj = FileClass()

        with mock.patch('baseclasses.artefact.expandfilepath', MagicMock(return_value=expected_file_path)):
            fileobj.source_path = '~/somepath'
            actual_file_path = fileobj.source_path

        self.assertEqual(expected_file_path, actual_file_path)

    def test_failpath_setter(self):
        """
        Should set the value of _filepath
        :return:
        """
        from baseclasses.artefact import FileClass

        expected_file_path = "./somepath"
        fileobj = FileClass()

        fileobj.source_path = './somepath'
        actual_file_path = fileobj._source_path

        self.assertEqual(expected_file_path, actual_file_path)

    def test_filepath_getter(self):
        """
        Should return the value of _filepath
        :return:
        """
        from baseclasses.artefact import FileClass

        expected_file_path = "./somepath"
        fileobj = FileClass()

        fileobj._source_path = './somepath'
        actual_file_path = fileobj.source_path

        self.assertEqual(expected_file_path, actual_file_path)


class TestToolClassToolPathGetter(TestCase):
    def test_tool_path_with_empty__tool_path(self):
        """
        Should return 'plutil' indicating that the live plutil is used.
        :return:
        """
        from baseclasses.artefact import ToolClass

        expected_tool_path = "plutil"
        tool = ToolClass()
        tool._default_tool = "plutil"
        actual_tool_path = tool.tool_path

        self.assertEqual(expected_tool_path, actual_tool_path)


class TestToolClassToolPathSetter(TestCase):
    @patch('artefact.localhost.tools.path.exists', MagicMock(return_value=True))
    def test_tool_path_existing_path(self):
        """
        Should return tool path.
        """
        from baseclasses.artefact import ToolClass

        tool = ToolClass()
        tool._default_tool = "plutil"
        with patch('baseclasses.artefact.validate_file_signature', MagicMock(return_value=True)):
            expected_tool_path = "some_tool_path"
            tool.tool_path = expected_tool_path
            actual_tool_path = tool._tool_path

            self.assertEqual(expected_tool_path, actual_tool_path)

    def test_tool_path_is_empty(self):
        """
        Should set _tool_path to empty string.
        :return:
        """
        from baseclasses.artefact import ToolClass

        expected_tool_path = ""
        tool = ToolClass()
        tool._default_path = "plutil"
        tool.tool_path = ""
        actual_tool_path = tool._tool_path

        self.assertEqual(expected_tool_path, actual_tool_path)

    @patch('artefact.localhost.tools.path.exists', MagicMock(return_value=True))
    def test_tool_path_exisiting_path_but_wrong_signature(self):
        """
        Should throw an exception.
        :return:
        """
        from baseclasses.artefact import ToolClass
        from businesslogic.errors import SignatureMatchError

        tool = ToolClass()
        tool._default_tool = "plutil"
        with patch('baseclasses.artefact.validate_file_signature', MagicMock(return_value=False)):
            expected_util_path = 'some_tool_path'
            with self.assertRaises(SignatureMatchError):
                tool.tool_path = expected_util_path

    def test_tool_path_does_not_exist(self):
        """
        Should not set the attribute _tool_path
        :return:
        """
        from baseclasses.artefact import ToolClass

        expected_tool_path = ""
        tool = ToolClass()
        tool._default_path = "plutil"
        tool.tool_path = "IDoNotExist"
        actual_tool_path = tool._tool_path

        self.assertEqual(expected_tool_path, actual_tool_path)

