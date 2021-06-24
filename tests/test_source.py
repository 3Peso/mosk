from unittest import TestCase

from baseclasses.source import SourceBase
from businesslogic.placeholders import Placeholder


class TestSourceBaseGetParameter(TestCase):
    def test_get_parameter_with_placeholder(self):
        """
        Should replace a placeholder with the value in the global placeholder dictionary.
        :return:
        """
        expected_value = "replaced"
        expected_parameter = "replace"
        Placeholder._instruction_placeholders[expected_parameter] = expected_value

        source = SourceBase(parent=None,
                            parameters={
                                "replace": f"{Placeholder.PLACEHOLDER_START}replace{Placeholder.PLACEHOLDER_END}"})
        actual_value = source.get_parameter(expected_parameter)

        self.assertEqual(expected_value, actual_value)

    def test_get_parameter_with_existing_parameter(self):
        """
        Should return the value of the exsiting parameter.
        :return:
        """
        expected_value = "expected"
        expected_parameter = "replace"
        Placeholder._instruction_placeholders[expected_parameter] = expected_value

        source = SourceBase(parent=None,
                            parameters={
                                expected_parameter: expected_value})
        actual_value = source.get_parameter(expected_parameter)

        self.assertEqual(expected_value, actual_value)

    def test_get_parameter_with_none_existing_parameter(self):
        """
        Should raise KeyError.
        :return:
        """
        source = SourceBase(parent=None, parameters={})
        self.assertRaises(KeyError, source.get_parameter, "does_not_exist")
