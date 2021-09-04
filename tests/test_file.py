from unittest import TestCase


class TestFileContentCollect(TestCase):
    def test__collect_file_does_not_exist(self):
        """
        Should store a message in data, that says that the file from which the content should be
        collected, does not exist.
        :return:
        """
        self.fail()

    def test__collect(self):
        """
        Should store the content of the target file inside the log.
        :return:
        """
        self.fail()

    def test__collect_file_bigger_than_10MB(self):
        """
        Should store a message in data, which says, that the file is to big for its content to be stored
        inside the collection log.
        :return:
        """
        self.fail()


class TestFileCopyDunderInit(TestCase):
    def test___init__(self):
        """
        Should do nothing.
        :return:
        """
        self.fail()


class TestFileCopyCollect(TestCase):
    def test__collect(self):
        """
        Should copy the file, identified by the member 'filepath'.
        :return:
        """
        self.fail()

    def test__collect_log_data(self):
        """
        Should log inside data which file was copied and what is the target destination of the copy.
        Should collect the md5 hash of the file, and the sha1 hash of the file.
        :return:
        """
        self.fail()

    def test__collect_destination_full(self):
        """
        If the file to be copied is to large for the destination, a message should be collected
        stating, that the copy could not happen. Only a stub file should be created at destination
        instead.
        :return:
        """
        self.fail()

    def test__collect_file_does_not_exist(self):
        """
        Should store a message in data, that says that the file from which the content should be
        collected, does not exist.
        :return:
        """
        self.fail()

    def test__collect_copy_inside_unique_sub_dir(self):
        """
        Stores copy of file inside a uniquely named sub dir of target dir.
        :return:
        """
        self.fail()


class TestFileCopySupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        self.fail()


class TestFileMetadataDunderInit(TestCase):
    def test___init(self):
        """
        Should do nothing.
        :return:
        """
        self.fail()


class TestFileMetadataCollect(TestCase):
    def test__collect(self):
        """
        Should collect metadata of a file inside data.
        :return:
        """
        self.fail()


class TestFileMetadataSupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        self.fail()