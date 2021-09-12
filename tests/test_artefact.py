import logging
from unittest import TestCase, mock
from unittest.mock import MagicMock


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
        from artefact.localhost.user import CurrentUser
        artefact = CurrentUser(parent=None, parameters={})

        self.assertEqual(artefact._title, 'CurrentUser')
        self.assertEqual(artefact._description, 'Collects the current user with the Python module getpass.')
        self.assertEqual(artefact._collectionmethod, 'getpass.getuser')


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
        actual_artefact._supportedplatform = None
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

        expected_message = 'The platform "Darwin" is not supported by this collector. ' \
                           '\r\nPlatform supported: "MamboJamboPlatform"'
        actual_artefact = ExceptionArtefactMockup(parent=None, parameters={})

        # Collect by using __call__
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