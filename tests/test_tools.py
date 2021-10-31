from unittest import TestCase


class TestPLUtilCollectInit(TestCase):
    def test___init__(self):
        """
        Should initialize property tool_path with empty string.
        :return:
        """
        self.fail()


class TestPLUtilCollect(TestCase):
    def test__collect_no_tool_path_provided(self):
        """
        Should use the plutil of the live artefact.
        Data should contain the warning.
        :return:
        """
        self.fail()

    def test__collect_no_filepath_provided(self):
        """
        Data should contain message that the provided plist file does not exist.
        :return:
        """
        self.fail()

    def test__collect_filepath_points_to_file_with_wrong_format(self):
        """
        Data should contain message that states that the file format is wrong.
        :return:
        """
        self.fail()

    def test__collect_filepath_has_unsupported_extension(self):
        """
        Data should contain message, that the file extension is not supported.
        :return:
        """
        self.fail()

    def test__collect_on_existing_plist_file(self):
        """
        Data should contain redable contents of the plist file.
        :return:
        """
        self.fail()


class TestPLUtilGetToolPath(TestCase):
    def test_tool_path_existing_path(self):
        """
        Should return tool path.
        """
        self.fail()

    def test_tool_path_exisiting_path_but_wrong_signature(self):
        """
        Should return 'plutil'
        :return:
        """
        self.fail()
