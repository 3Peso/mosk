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
        self.fail()

    def test_cache_parameters_already_defined(self):
        """
        Should overwrite the placeholder in the global placeholders dictionary of Placeholders.
        """
        self.fail()
