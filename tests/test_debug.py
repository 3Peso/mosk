from unittest import TestCase

from businesslogic.placeholders import Placeholder


class TestDebugCollect(TestCase):
    def setUp(self) -> None:
        Placeholder.GLOBAL_PLACEHOLDER_FILE_PATH = "./global_placeholders.json"
        Placeholder._initialize_global_placeholders()

    def test__collect_with_existing_placeholder(self):
        """
        Should write global placeholder value into _data member.
        :return:
        """
        from artefact.support.debug import DebugPlaceholder

        expected_placeholder_value = "test value"
        expected_placeholder_name = "test"
        debug_placeholder = DebugPlaceholder(parent=None, parameters={'placeholder': f"{expected_placeholder_name}"})
        Placeholder._instruction_placeholders[expected_placeholder_name] = expected_placeholder_value

        debug_placeholder._collect()
        actual_value = debug_placeholder.data[0].collecteddata

        self.assertEqual(expected_placeholder_value, actual_value)

    def test__collect_with_none_existing_placeholer(self):
        """
        Should write error message into _data member.
        :return:
        """
        from artefact.support.debug import DebugPlaceholder

        expected_value = "The placeholder 'does not exist' has not been initialized yet."
        debug_placeholder = DebugPlaceholder(parent=None, parameters={'placeholder': "does not exist"})

        debug_placeholder._collect()
        actual_value = debug_placeholder.data[0].collecteddata

        self.assertEqual(expected_value, actual_value)
