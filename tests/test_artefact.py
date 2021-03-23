from unittest import TestCase, mock
from unittest.mock import MagicMock


class TestArtefactBase(TestCase):

    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    @mock.patch('baseclasses.source.SourceBase.cache_parameters', MagicMock())
    def test_data_setter(self):
        """
        Should add the provided value as data object to its data object list
        :return:
        """
        from baseclasses.artefact import ArtefactBase
        artefact = ArtefactBase(parent=None, parameters={})
        artefact.data = "Some data"

        assert len(artefact.data) == 1

    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    @mock.patch('baseclasses.source.SourceBase.cache_parameters', MagicMock())
    def test_data_setter_with_two_objects(self):
        """
        Should append data to the data object array if there are more data objects to be collected
        :return:
        """
        from baseclasses.artefact import ArtefactBase
        artefact = ArtefactBase(parent=None, parameters={})
        artefact.data = "Some data"
        artefact.data = "More data"

        assert len(artefact.data) == 2

    @mock.patch('businesslogic.placeholders.Placeholder._initialize_global_placeholders', MagicMock())
    @mock.patch('baseclasses.source.SourceBase.cache_parameters', MagicMock())
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

        assert len(artefact.data) == 0
