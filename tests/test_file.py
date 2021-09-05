import os
import os.path
import shutil
from collections import namedtuple

from unittest import TestCase, mock
from unittest.mock import MagicMock


class TestFileContentCollect(TestCase):
    def test__collect_file_does_not_exist(self):
        """
        Should store a message in data, that says that the file from which the content should be
        collected, does not exist.
        :return:
        """
        from artefact.localhost.file import FileContent

        expected_file = "./IDoNotExist.txt"
        expected_data = f"File '{expected_file}' does not exist."
        collector = FileContent(parameters={}, parent={})
        collector.filepath = expected_file
        collector._collect()

        self.assertEqual(expected_data, collector.data[0].collecteddata)

    def test__collect(self):
        """
        Should store the content of the target file inside the log.
        :return:
        """
        from artefact.localhost.file import FileContent

        expected_file = "./testfiles/test.txt"
        expected_data = "This is a test file.\n\nIt should be used to test\nworking with file content."
        collector = FileContent(parameters={}, parent={})
        collector.filepath = expected_file
        collector._collect()

        self.assertEqual(expected_data, collector.data[0].collecteddata)


class TestFileContentReadFile(TestCase):
    def test__read_file_with_too_large_file(self):
        """
        Should store a message in data, which says, that the file is to big for its content to be stored
        inside the collection log.
        :return:
        """
        from collections import namedtuple
        from artefact.localhost.file import FileContent

        expected_file = "dummyfile.txt"
        expected_data = f"File '{expected_file}' is bigger than {FileContent._max_file_size/1024/1024} MiBs. " \
                        f"File Content Collector max file size is {FileContent._max_file_size/1024/1024} MiBs."
        collector = FileContent(parameters={}, parent={})
        Mock_Stats = namedtuple('Mock_Stats', ['st_size'])
        mock_stats = Mock_Stats(st_size=1024*1024*10+1)
        with mock.patch('artefact.localhost.file.Path.stat', MagicMock(return_value=mock_stats)):
            with mock.patch('artefact.localhost.file.path.exists', MagicMock(return_value=True)):
                collector._read_file(filepath=expected_file, filetoload=None)

        self.assertEqual(expected_data, collector.data[0].collecteddata)


class TestFileContentDunderInit(TestCase):
    def test___init___max_file_size(self):
        """
        Should be by default 10 MiBs
        :return:
        """
        expected_size = 10485760 # which is 10 MiBs
        from artefact.localhost.file import FileContent
        collector = FileContent(parameters={}, parent={})

        self.assertEqual(expected_size, collector._max_file_size)


class TestFileCopyDunderInit(TestCase):
    def test___init___targert_directory(self):
        """
        By default _target_directory should be set to '.'
        :return:
        """
        from artefact.localhost.file import FileCopy
        expected_target_dir = '.'
        collector = FileCopy(parameters={}, parent=None)

        self.assertEqual(expected_target_dir, collector._destination_directory)


class TestFileCopyCollect(TestCase):
    _expected_source_file_path = './testfiles/test.txt'
    _expected_target_directory = '.'
    _expected_unique_directory = 'unique'

    def setUp(self) -> None:
        self._expected_source_file_name = os.path.basename(self._expected_source_file_path)
        target_path = os.path.join(self._expected_target_directory, self._expected_unique_directory)
        self._expected_target_file_path = os.path.join(target_path, self._expected_source_file_name)
        self._expected_target_path = target_path

    def tearDown(self) -> None:
        shutil.rmtree(self._expected_target_path, True)

    def test__collect(self):
        """
        Should copy the file, identified by the member 'filepath'.
        :return:
        """
        from artefact.localhost.file import FileCopy

        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = self._expected_source_file_path
        with mock.patch('artefact.localhost.file.FileCopy._ensure_target_directory',
                        MagicMock(return_value=self._expected_target_path)):
            # Create the target path here, because we mocked _ensure_target_directory
            if not os.path.exists(self._expected_target_path):
                os.mkdir(self._expected_target_path)
            collector._collect()

        self.assertTrue(os.path.exists(self._expected_target_file_path))

    def test__collect_log_data(self):
        """
        Should log inside data which file was copied and what is the target destination of the copy.
        Should collect the md5 hash of the file, and the sha1 hash of the file.
        :return:
        """
        from artefact.localhost.file import FileCopy

        expected_data = f"Copied file '{self._expected_source_file_path}' to '{self._expected_target_file_path}'."
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = self._expected_source_file_path
        with mock.patch('artefact.localhost.file.FileCopy._ensure_target_directory',
                        MagicMock(return_value=self._expected_target_path)):
            # Create the target path here, because we mocked _ensure_target_directory
            if not os.path.exists(self._expected_target_path):
                os.mkdir(self._expected_target_path)
            collector._collect()
        actual_data = collector.data[0].collecteddata

        self.assertEqual(expected_data, actual_data)

    @mock.patch('artefact.localhost.file.FileCopy._enough_space_on_target', MagicMock(return_value=True))
    def test__collect_file_does_not_exist(self):
        """
        Should store a message in data, that says that the file from which the content should be
        collected, does not exist.
        :return:
        """
        from artefact.localhost.file import FileCopy

        expected_source_file_path = "./somedir/IDoNotExist.txt"
        expected_data = f"The file '{expected_source_file_path}' does not exist."
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = expected_source_file_path
        with mock.patch('artefact.localhost.file.FileCopy._ensure_target_directory',
                        MagicMock(return_value=self._expected_target_path)):
            collector._collect()
        actual_data = collector.data[0].collecteddata

        self.assertEqual(expected_data, actual_data)

    @mock.patch('artefact.localhost.file.FileCopy._enough_space_on_target', MagicMock(return_value=True))
    def test__collect_could_not_copy_file(self):
        """
        Should ensure that unique target directory is deleted.
        :return:
        """
        from artefact.localhost.file import FileCopy

        expected_source_file_path = f"{self._expected_unique_directory}/IDoNotExist.txt"
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = expected_source_file_path
        with mock.patch('artefact.localhost.file.FileCopy._ensure_target_directory',
                        MagicMock(return_value=self._expected_target_path)):
            # Create the target path here, because we mocked _ensure_target_directory
            if not os.path.exists(self._expected_target_path):
                os.mkdir(self._expected_target_path)
            collector._collect()

        self.assertFalse(os.path.exists(self._expected_target_path))


class TestFileCopyFilePath(TestCase):
    def test__collect_setter_with_abreviated_path(self):
        """
        Should expand the targert file path, if the file path provided is an abreviation, like
        for example ~/test.txt
        :return:
        """
        from pathlib import Path
        from artefact.localhost.file import FileCopy

        source_file_path = "~/IDoNotExist.txt"
        expected_file_path = f"{str(Path.home())}/IDoNotExist.txt"
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = source_file_path
        actual_filepath = collector._filepath

        self.assertEqual(expected_file_path, actual_filepath)


class TestFileCopyEnsureTargetDirectory(TestCase):
    def test__ensure_target_directory(self):
        """
        Should return path of unique target directory
        :return:
        """
        import os.path
        from artefact.localhost.file import FileCopy

        expected_target_dir = "./test_target"
        expected_unique_dir_name = "me_unique"
        expected_return_value = './test_target/me_unique'
        collector = FileCopy(parameters={}, parent=None)
        collector._destination_directory = expected_target_dir
        try:
            with mock.patch('artefact.localhost.file.FileCopy._get_unique_directory_name',
                            MagicMock(return_value=expected_unique_dir_name)):
                acutal_return_value = collector._ensure_target_directory()
                self.assertEqual(expected_return_value, acutal_return_value)
        finally:
            if(os.path.exists(os.path.join(expected_target_dir, expected_unique_dir_name))):
                os.rmdir(os.path.join(expected_target_dir, expected_unique_dir_name))
            if os.path.exists(expected_target_dir):
                os.rmdir(expected_target_dir)

    def test__ensure_target_directory_target_does_not_exist(self):
        """
        Should create target directory, if it does not exist.
        :return:
        """
        import os.path
        from artefact.localhost.file import FileCopy

        expected_target_dir = "./test_target"
        expected_unique_dir_name = "me_unique"
        collector = FileCopy(parameters={}, parent=None)
        collector._destination_directory = expected_target_dir
        try:
            with mock.patch('artefact.localhost.file.FileCopy._get_unique_directory_name',
                            MagicMock(return_value=expected_unique_dir_name)):
                collector._ensure_target_directory()
            self.assertTrue(os.path.exists(expected_target_dir))
        finally:
            if(os.path.exists(os.path.join(expected_target_dir, expected_unique_dir_name))):
                os.rmdir(os.path.join(expected_target_dir, expected_unique_dir_name))
            if os.path.exists(expected_target_dir):
                os.rmdir(expected_target_dir)

    def test__ensure_target_directory_unique_inside_target_dir(self):
        """
        Should create directory with unique name inside target directory.
        :return:
        """
        import os.path
        from artefact.localhost.file import FileCopy

        expected_target_dir = "./test_target"
        expected_unique_dir_name = "me_unique"
        collector = FileCopy(parameters={}, parent=None)
        collector._destination_directory = expected_target_dir
        try:
            with mock.patch('artefact.localhost.file.FileCopy._get_unique_directory_name',
                            MagicMock(return_value=expected_unique_dir_name)):
                collector._ensure_target_directory()
            self.assertTrue(os.path.exists(
                os.path.join(expected_target_dir, expected_unique_dir_name)))
        finally:
            if os.path.exists(os.path.join(expected_target_dir, expected_unique_dir_name)):
                os.rmdir(os.path.join(expected_target_dir, expected_unique_dir_name))
            if(os.path.exists(expected_target_dir)):
                os.rmdir(expected_target_dir)

class TestFileCopyGetUniqueDirectoryName(TestCase):
    @mock.patch('artefact.localhost.file.path.exists', MagicMock(return_value=False))
    @mock.patch('artefact.localhost.file.ArtefactBase._init_description_properties', MagicMock())
    def test__get_unique_directory_name(self):
        """
        Should return directory name which is unique to target directory using
        file name, datetime stamp, and counter
        :return:
        """
        from datetime import datetime
        from artefact.localhost.file import FileCopy
        expected_time = datetime(2009, 3, 20, 13, 12, 2)
        expected_dir_name = 'some_file.txt_2009032013120201'
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = '~/somepath/some_file.txt'
        actual_dir_name = collector._get_unique_directory_name('mock', expected_time)

        self.assertEqual(expected_dir_name, actual_dir_name)

    def test__get_unique_directory_name_timestamp_already_taken(self):
        """
        Should return a unique name with the same datetime stamp but with the
        counter incremented by one
        :return:
        """
        import os
        from datetime import datetime
        from artefact.localhost.file import FileCopy
        expected_time = datetime(2009, 3, 20, 13, 12, 2)
        expected_dir_name = 'some_file.txt_2009032013120202'
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = '~/somepath/some_file.txt'
        try:
            os.mkdir('./some_file.txt_2009032013120201')
            actual_dir_name = collector._get_unique_directory_name('.', expected_time)
        finally:
            os.rmdir('./some_file.txt_2009032013120201')

        self.assertEqual(expected_dir_name, actual_dir_name)

    @mock.patch('artefact.localhost.file.path.exists', MagicMock(return_value=True))
    def test__get_unique_directory_name_max_counter_reached(self):
        """
        Should raise an exception.
        :return:
        """
        from datetime import datetime
        from artefact.localhost.file import FileCopy
        expected_time = datetime(2009, 3, 20, 13, 12, 2)
        expected_dir_name = 'some_file.txt_2009032013120201'
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = '~/somepath/some_file.txt'
        self.assertRaises(OverflowError, collector._get_unique_directory_name, '.', expected_time)


class TestFileCopyEnoughSpaceOnTarget(TestCase):
    @mock.patch('artefact.localhost.file.os.path.exists', MagicMock(return_value=True))
    def test__enough_space_on_target_suffice_space(self):
        """
        Should return true.
        :return:
        """
        from artefact.localhost.file import FileCopy

        MockedDiskUsage = namedtuple('MockedDiskUsage',['free'])
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = './testfiles/test.txt'
        with mock.patch('artefact.localhost.file.shutil.disk_usage',
                        MagicMock(return_value=MockedDiskUsage(free=100000))):
            self.assertTrue(collector._enough_space_on_target('.'))

    @mock.patch('artefact.localhost.file.os.path.exists', MagicMock(return_value=True))
    def test__enough_space_on_target_not_enough(self):
        """
        Should return false.
        :return:
        """
        from artefact.localhost.file import FileCopy

        MockedDiskUsage = namedtuple('MockedDiskUsage',['free'])
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = './testfiles/test.txt'
        with mock.patch('artefact.localhost.file.shutil.disk_usage',
                        MagicMock(return_value=MockedDiskUsage(free=1))):
            self.assertFalse(collector._enough_space_on_target('.'))

    @mock.patch('artefact.localhost.file.os.path.exists', MagicMock(return_value=False))
    @mock.patch('artefact.localhost.file.ArtefactBase._init_description_properties', MagicMock())
    def test__enough_space_on_target_does_not_exist(self):
        """
        Should return false.
        :return:
        """
        from artefact.localhost.file import FileCopy

        MockedDiskUsage = namedtuple('MockedDiskUsage', ['free'])
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = './testfiles/test.txt'
        with mock.patch('artefact.localhost.file.shutil.disk_usage',
                        MagicMock(return_value=MockedDiskUsage(free=1000000))):
            self.assertFalse(collector._enough_space_on_target('.'))

    def test__enough_space_on_target_source_does_not_exist(self):
        """
        Should return false
        :return:
        """
        from artefact.localhost.file import FileCopy

        MockedDiskUsage = namedtuple('MockedDiskUsage', ['free'])
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = './testfiles/doesnotexist.txt'
        with mock.patch('artefact.localhost.file.shutil.disk_usage',
                        MagicMock(return_value=MockedDiskUsage(free=1000000))):
            self.assertFalse(collector._enough_space_on_target('.'))


class TestFileCopySupportedSystem(TestCase):
    def test__supportedsystem(self):
        """
        Should be "Darwin"
        :return:
        """
        from artefact.localhost.file import FileCopy
        collector = FileCopy(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedsystem)


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
        from artefact.localhost.file import FileMetadata
        collector = FileMetadata(parameters={}, parent={})

        self.assertEqual("Darwin", collector._supportedsystem)