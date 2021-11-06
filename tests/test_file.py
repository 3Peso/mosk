import os
import os.path
import platform
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
        expected_data = f"File '{expected_file}' is bigger than {FileContent._max_file_size / 1024 / 1024} MiBs. " \
                        f"File Content Collector max file size is {FileContent._max_file_size / 1024 / 1024} MiBs."
        collector = FileContent(parameters={}, parent={})
        Mock_Stats = namedtuple('Mock_Stats', ['st_size'])
        mock_stats = Mock_Stats(st_size=1024 * 1024 * 10 + 1)
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
        expected_size = 10485760  # which is 10 MiBs
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
    def test__collect_with_one_file(self):
        """
        Should call _collect_single
        :return:
        """
        from artefact.localhost.file import FileCopy

        collector = FileCopy(parameters={}, parent=None)

        single_mock: MagicMock = MagicMock()
        with mock.patch('artefact.localhost.file.FileCopy._collect_single', single_mock):
            collector._filepath = "/somepath"
            collector._collect()

        single_mock.assert_called_once()

    def test__collect_with_two_files(self):
        """
        Should call _collect_single two times.
        :return:
        """
        from artefact.localhost.file import FileCopy

        collector = FileCopy(parameters={}, parent=None)
        expected_file_path = f"/SomePath{FileCopy._FILE_PATH_SEPERATOR}/Another Path"
        collector.filepath = expected_file_path

        expected_call_count = 2
        single_mock: MagicMock = MagicMock()
        with mock.patch('artefact.localhost.file.FileCopy._collect_single', single_mock):
            collector._collect()

        self.assertEqual(expected_call_count, single_mock.call_count)


class TestFileCopyCollectSingle(TestCase):
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

    def test__collect_single(self):
        """
        Should copy the file, identified by the member 'filepath'.
        :return:
        """
        from artefact.localhost.file import FileCopy

        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = self._expected_source_file_path
        with mock.patch('artefact.localhost.file.os.path.isfile', MagicMock(return_value=True)):
            with mock.patch('artefact.localhost.file.FileCopy._ensure_target_directory',
                            MagicMock(return_value=self._expected_target_path)):
                # Create the target path here, because we mocked _ensure_target_directory
                if not os.path.exists(self._expected_target_path):
                    os.mkdir(self._expected_target_path)
                collector._collect_single(collector.filepath)

        self.assertTrue(os.path.exists(self._expected_target_file_path))

    def test__collect_single_log_data(self):
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
            collector._collect_single(collector.filepath)
        actual_data = collector.data[0].collecteddata

        self.assertEqual(expected_data, actual_data)

    @mock.patch('artefact.localhost.file.FileCopy._enough_space_on_target', MagicMock(return_value=True))
    def test__collect_single_file_does_not_exist(self):
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
        with mock.patch('artefact.localhost.file.os.path.isfile', MagicMock(return_value=True)):
            with mock.patch('artefact.localhost.file.FileCopy._ensure_target_directory',
                            MagicMock(return_value=self._expected_target_path)):
                collector._collect_single(file_path=collector.filepath)
            actual_data = collector.data[0].collecteddata

        self.assertEqual(expected_data, actual_data)

    @mock.patch('artefact.localhost.file.FileCopy._enough_space_on_target', MagicMock(return_value=True))
    def test__collect_single_could_not_copy_file(self):
        """
        Should ensure that unique target directory is deleted.
        :return:
        """
        from artefact.localhost.file import FileCopy

        expected_source_file_path = f"{self._expected_unique_directory}/IDoNotExist.txt"
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = expected_source_file_path
        collector._collect_single()

        self.assertFalse(os.path.exists(self._expected_target_path))

    def test__collect_single_filepath_is_a_directory(self):
        """
        Should "collect" an error message which states that the "filepath" provided is actually a directory.
        :return:
        """
        from artefact.localhost.file import FileCopy

        expected_file = "/iamnotafile"
        expected_message = f"The provided filepath '{expected_file}' is not a file."
        collector = FileCopy(parameters={'filepath': expected_file}, parent=None)
        collector._collect_single(file_path=expected_file)

        actual_message = collector.data[0].collecteddata

        self.assertEqual(expected_message, actual_message)

    def test__collect_single_filepath_to_long_for_windows(self):
        """
        Should "collect" an error message which states that the target path is too long for the underlying
        platform.
        :return:
        """
        from artefact.localhost.file import FileCopy

        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = self._expected_source_file_path
        expected_message = "File './testfiles/test.txt' could not be copied, because the target path length of " \
                           "'./unique' is too long for the underlying system."
        if platform.system() == "Windows":
            expected_message = "File './testfiles/test.txt' could not be copied, because the target path length of " \
                               "'.\\unique' is too long for the underlying system."

        with mock.patch('artefact.localhost.file.os.path.isfile', MagicMock(return_value=True)):
            with mock.patch('artefact.localhost.file.FileCopy._ensure_target_directory',
                            MagicMock(return_value=self._expected_target_path)):
                with mock.patch('artefact.localhost.file.FileCopy._validate_target_path_length',
                                MagicMock(return_value=False)):
                    collector._collect_single(collector.filepath)
                    actual_message = collector.data[-1].collecteddata

        self.assertEqual(expected_message, actual_message)


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
        if platform.system() == "Windows":
            expected_file_path = f"{str(Path.home())}\IDoNotExist.txt"
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = source_file_path
        actual_filepath = collector._filepath

        self.assertEqual(expected_file_path, actual_filepath)

    def test__collect_getter_with_newline_at_the_end(self):
        """
        Should sanitize the file path. There must not be any new line, carriage return, etc. at
        the end. Otherwise things like os.path.exists do not work.
        :return:
        """
        from artefact.localhost.file import FileCopy

        expected_file_path = "./somepath"

        with mock.patch('artefact.localhost.file.os.path.exists', MagicMock(return_value=True)):
            collector = FileCopy(parameters={'filepath': './somepath\r\n'}, parent=None)

        actual_file_path = collector.filepath

        self.assertEqual(expected_file_path, actual_file_path)


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
        if platform.system() == "Windows":
            expected_return_value = './test_target\\me_unique'
        collector = FileCopy(parameters={}, parent=None)
        collector._destination_directory = expected_target_dir
        try:
            with mock.patch('artefact.localhost.file.FileCopy._get_unique_directory_name',
                            MagicMock(return_value=expected_unique_dir_name)):
                acutal_return_value = collector._ensure_target_directory()
                self.assertEqual(expected_return_value, acutal_return_value)
        finally:
            if os.path.exists(os.path.join(expected_target_dir, expected_unique_dir_name)):
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
            if os.path.exists(os.path.join(expected_target_dir, expected_unique_dir_name)):
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
            if os.path.exists(expected_target_dir):
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
        from businesslogic.errors import MaxDirectoriesReachedError
        from artefact.localhost.file import FileCopy
        expected_time = datetime(2009, 3, 20, 13, 12, 2)
        expected_dir_name = 'some_file.txt_2009032013120201'
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = '~/somepath/some_file.txt'
        self.assertRaises(MaxDirectoriesReachedError, collector._get_unique_directory_name, '.', expected_time)


class TestFileCopyEnoughSpaceOnTarget(TestCase):
    @mock.patch('artefact.localhost.file.os.path.exists', MagicMock(return_value=True))
    def test__enough_space_on_target_suffice_space(self):
        """
        Should return true.
        :return:
        """
        from artefact.localhost.file import FileCopy

        MockedDiskUsage = namedtuple('MockedDiskUsage', ['free'])
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = './testfiles/test.txt'
        with mock.patch('artefact.localhost.file.shutil.disk_usage',
                        MagicMock(return_value=MockedDiskUsage(free=100000))):
            self.assertTrue(collector._enough_space_on_target(target_path='.', source_path=collector.filepath))

    @mock.patch('artefact.localhost.file.os.path.exists', MagicMock(return_value=True))
    def test__enough_space_on_target_not_enough(self):
        """
        Should return false.
        :return:
        """
        from artefact.localhost.file import FileCopy

        MockedDiskUsage = namedtuple('MockedDiskUsage', ['free'])
        collector = FileCopy(parameters={}, parent=None)
        collector.filepath = './testfiles/test.txt'
        with mock.patch('artefact.localhost.file.shutil.disk_usage',
                        MagicMock(return_value=MockedDiskUsage(free=1))):
            self.assertFalse(collector._enough_space_on_target(target_path='.', source_path=collector.filepath))

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
            self.assertFalse(collector._enough_space_on_target(target_path='.', source_path=collector.filepath))

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
            self.assertFalse(collector._enough_space_on_target(target_path='.', source_path=collector.filepath))


class TestFileCopySupportedPlatform(TestCase):
    def test__supportedplatform_on_darwin(self):
        """
        Should support "Darwin"
        :return:
        """
        from artefact.localhost.file import FileCopy

        expected_support = True
        with mock.patch('artefact.localhost.file.platform.system', MagicMock(return_value='Darwin')):
            collector = FileCopy(parameters={}, parent={})
            actual_support = collector.is_platform_supported()

        self.assertEqual(expected_support, actual_support)

    def test__supportedplatform_on_linux(self):
        """
        Should suport "Linux"
        :return:
        """
        from artefact.localhost.file import FileCopy

        expected_support = True
        with mock.patch('artefact.localhost.file.platform.system', MagicMock(return_value='Linux')):
            collector = FileCopy(parameters={}, parent={})
            actual_support = collector.is_platform_supported()

        self.assertEqual(expected_support, actual_support)


class TestFileMetadataDunderInit(TestCase):
    def test___init(self):
        """
        Should initialize filepath.
        :return:
        """
        from artefact.localhost.file import FileMetadata

        expected_filepath = "IDoNotExist.txt"
        collector = FileMetadata(parameters={'filepath': expected_filepath}, parent={})
        collector._collect()

        self.assertEqual(expected_filepath, collector.filepath)


class TestFileMetadataCollect(TestCase):
    def test__collect_file_does_not_exist(self):
        """
        Should store info about not existing file in data.
        :return:
        """
        from artefact.localhost.file import FileMetadata

        expected_filepath = "IDoNotExist.txt"
        expected_data = f"File '{expected_filepath}' does not exist."
        collector = FileMetadata(parameters={}, parent={})
        collector.filepath = expected_filepath
        collector._collect()
        actual_data = collector.data[0].collecteddata

        self.assertEqual(expected_data, actual_data)


class TestFileMetadataCollectTimestamps(TestCase):
    def test__collect_timestamps_accessed_time(self):
        """
        Should collect used timestamp in data.
        :return:
        """
        from artefact.localhost.file import FileMetadata

        expected_access_time_data = "2021-06-04 08:33:32 UTC"
        expected_file = './testfiles/test.txt'

        collector = FileMetadata(parameters={}, parent=None)
        collector.filepath = expected_file
        with mock.patch('artefact.localhost.file.os.path.getatime', MagicMock(return_value=1622795612.874454)):
            collector._collect_timestamps()

        actual_access_time_data = collector._metadata['Accessed']

        self.assertEqual(expected_access_time_data, actual_access_time_data)

    def test__collect_timestamps_created_time(self):
        """
        Should collect used timestamp in data.
        :return:
        """
        from artefact.localhost.file import FileMetadata

        expected_created_time_data = "2021-06-04 08:33:32 UTC"
        expected_file = './testfiles/test.txt'

        collector = FileMetadata(parameters={}, parent=None)
        collector.filepath = expected_file
        with mock.patch('artefact.localhost.file.os.path.getctime', MagicMock(return_value=1622795612.874454)):
            collector._collect_timestamps()

        actual_created_time_data = collector._metadata['Created']

        self.assertEqual(expected_created_time_data, actual_created_time_data)

    def test__collect_timestamps_accessed_time(self):
        """
        Should collect used timestamp in data.
        :return:
        """
        from artefact.localhost.file import FileMetadata

        expected_modified_time_data = "2021-06-04 08:33:32 UTC"
        expected_file = './testfiles/test.txt'

        collector = FileMetadata(parameters={}, parent=None)
        collector.filepath = expected_file
        with mock.patch('artefact.localhost.file.os.path.getmtime', MagicMock(return_value=1622795612.874454)):
            collector._collect_timestamps()

        actual_modified_time_data = collector._metadata['Modified']

        self.assertEqual(expected_modified_time_data, actual_modified_time_data)

    @mock.patch('artefact.localhost.file.platform.system', MagicMock(return_value="Windows"))
    def test__collect_timestamps_platform_windows(self):
        """
        Should should throw KeyError when accessing 'Birth'
        :param self:
        :return:
        """
        from artefact.localhost.file import FileMetadata

        expected_file = './testfiles/test.txt'
        collector = FileMetadata(parameters={}, parent=None)
        collector.filepath = expected_file
        with mock.patch('artefact.localhost.file.os.path.getmtime', MagicMock(return_value=1622795612.874454)):
            collector._collect_timestamps()
            with self.assertRaises(KeyError):
                collector._metadata['Birth']


class TestFileMetadataCollectExtendedAttributes(TestCase):
    def test__collect_extended_attributes(self):
        """
        Should store extended attributes in data
        :return:
        """
        from artefact.localhost.file import FileMetadata

        expected_attribute = "my.extended.attribute"
        expected_message = f"Extended Attributes: {expected_attribute}"
        collector = FileMetadata(parameters={}, parent=None)
        collector.filepath = "mocked_file_path"
        with mock.patch('artefact.localhost.file.run_terminal_command',
                        MagicMock(return_value="my.extended.attribute")):
            collector._collect_extended_attributes()
            actual_message = collector.data[-1].collecteddata

        if platform.system() != "Windows":
            self.assertEqual(expected_message, actual_message)
        else:
            pass

    def test__collect_extended_attributes_on_windows(self):
        """
        Should return error message stating that this is not supported on windows.
        :return:
        """
        from artefact.localhost.file import FileMetadata

        expected_message = "Collection of extended attributes on platform 'Windows' is not supported."
        collector = FileMetadata(parameters={}, parent=None)
        collector.filepath = "mocked_file_path"
        with mock.patch('artefact.localhost.file.run_terminal_command',
                        MagicMock(return_value="my.extended.attribute")):
            with mock.patch('artefact.localhost.file.platform.system', MagicMock(return_value='Windows')):
                collector._collect_extended_attributes()
                actual_message = collector.data[-1].collecteddata

        self.assertEqual(expected_message, actual_message)

    def test__collect_extended_attributes_platform_not_darwin(self):
        """
        Should store message in data, that platform is not supported.
        :return:
        """
        from artefact.localhost.file import FileMetadata

        expected_platform = "Windows"
        expected_message = f"Collection of extended attributes on platform '{expected_platform}' is not supported."
        collector = FileMetadata(parameters={}, parent=None)
        with mock.patch('artefact.localhost.file.platform.system',
                        MagicMock(return_value=expected_platform)):
            collector._collect_extended_attributes()
            actual_message = collector.data[-1].collecteddata

        self.assertEqual(expected_message, actual_message)


class TestFileHashDunderInit(TestCase):
    def test___init__(self):
        """
        Should initialize members 'filepath' and 'hash'
        :return:
        """
        from artefact.localhost.file import FileHash

        expected_filepath = "some_path"
        expected_filehash = "12345"
        collector = FileHash(parent=None, parameters={'filepath': expected_filepath, 'filehash': expected_filehash})

        self.assertEqual(expected_filepath, collector.filepath)
        self.assertEqual(expected_filehash, collector.filehash)


class TestFileHashCollect(TestCase):
    def test__collect_invalid_hash(self):
        """
        Should write message in data that hash is invalid.
        :return:
        """
        from artefact.localhost.file import FileHash

        expected_hash = "12345"
        expected_message = f"MD5 hash '{expected_hash}' is invalid."
        collector = FileHash(parameters={'filehash': expected_hash, 'filepath': ''}, parent=None)
        collector._collect()

        actual_message = collector.data[0].collecteddata

        self.assertEqual(expected_message, actual_message)

    def test__collect_file_does_not_exist(self):
        """
        Should write message in data that file does not exist.
        :return:
        """
        from artefact.localhost.file import FileHash

        expected_hash = "00236a2ae558018ed13b5222ef1bd987"
        expected_file = "IDoNotExist.txt"
        expected_message = f"The file '{expected_file}' does not exist."
        collector = FileHash(parameters={'filehash': expected_hash, 'filepath': expected_file}, parent=None)
        collector._collect()

        actual_message = collector.data[0].collecteddata

        self.assertEqual(expected_message, actual_message)

    def test__collect_file_hash_not_identical(self):
        """
        Should write message in data, that the file hash does not match.
        :return:
        """
        from artefact.localhost.file import FileHash

        expected_hash = "00236a2ae558018ed13b5222ef1bd987"
        expected_file = "./testfiles/test.txt"
        file_hash = '0db7d1adf349b912f612c9be06278706'
        if platform.system() == "Windows":
            file_hash = 'eb9741896e5a38b773be6da56fe90c3a'

        expected_message = f"The hash '{file_hash}' of file '{expected_file}' does not match the provided hash " \
                           f"'{expected_hash}'."
        collector = FileHash(parameters={'filehash': expected_hash, 'filepath': expected_file}, parent=None)
        collector._collect()

        actual_message = collector.data[0].collecteddata

        self.assertEqual(expected_message, actual_message)

    def test__collect_file_hash_identical(self):
        """
        Should write message in data, that the file hash is identical.
        :return:
        """
        from artefact.localhost.file import FileHash

        expected_hash = "0db7d1adf349b912f612c9be06278706"
        if platform.system() == "Windows":
            expected_hash = 'eb9741896e5a38b773be6da56fe90c3a'

        expected_file = "./testfiles/test.txt"
        file_hash = '0db7d1adf349b912f612c9be06278706'
        if platform.system() == "Windows":
            file_hash = 'eb9741896e5a38b773be6da56fe90c3a'

        expected_message = f"The hash '{file_hash}' of file '{expected_file}' matches the provided hash " \
                           f"'{expected_hash}'."
        collector = FileHash(parameters={'filehash': expected_hash, 'filepath': expected_file}, parent=None)
        collector._collect()

        actual_message = collector.data[0].collecteddata

        self.assertEqual(expected_message, actual_message)


class TestFileCopyValidateTargetPathLength(TestCase):
    def test__validate_target_path_length_platform_is_windows_path_length_260(self):
        """
        Should return True
        :return:
        """
        from artefact.localhost.file import FileCopy

        collector = FileCopy(parent=None, parameters={})

        expected_target_path = f"D:\{'d' * 249}\file.txt"
        expected_result = True
        with mock.patch('artefact.localhost.file.platform.system', MagicMock(return_value="Windows")):
            actual_result = collector._validate_target_path_length(expected_target_path)

        self.assertEqual(expected_result, actual_result)

    def test__validate_target_path_length_platform_is_windows_path_length_261(self):
        """
        Should return False
        :return:
        """
        from artefact.localhost.file import FileCopy

        collector = FileCopy(parent=None, parameters={})

        expected_target_path = f"D:\{'d' * 250}\file.txt"
        expected_result = False
        with mock.patch('artefact.localhost.file.platform.system', MagicMock(return_value="Windows")):
            actual_result = collector._validate_target_path_length(expected_target_path)

        self.assertEqual(expected_result, actual_result)

    def test__validate_target_path_length_platform_is_not_windows(self):
        """
        Should return True
        :return:
        """
        from artefact.localhost.file import FileCopy

        collector = FileCopy(parent=None, parameters={})

        expected_target_path = f"/{'d' * 300}/file.txt"
        expected_result = True
        with mock.patch('artefact.localhost.file.platform.system', MagicMock(return_value="Darwin")):
            actual_result = collector._validate_target_path_length(expected_target_path)

        self.assertEqual(expected_result, actual_result)


class TestFileCopyDestinationDirectoryGetter(TestCase):
    def test_destination_directory_default(self):
        """
        By default, it should return '.'.
        :return:
        """
        from artefact.localhost.file import FileCopy

        expected = '.'
        file_ = FileCopy(parameters={}, parent=None)
        actual = file_.destination_directory

        self.assertEqual(expected, actual)


class TestFileCopyDestinationDirectorySetter(TestCase):
    def test_destination_directory_exists(self):
        """
        Should set the property _destination_directory
        :return:
        """
        from artefact.localhost.file import FileCopy

        expected = './copydestination/'
        file_ = FileCopy(parameters={}, parent=None)
        file_.destination_directory = expected
        actual = file_._destination_directory

        self.assertEqual(expected, actual)

    def test_destination_directory_does_not_exist(self):
        """
        Should raise an execption.
        :return:
        """
        from artefact.localhost.file import FileCopy

        file_ = FileCopy(parameters={}, parent=None)
        with self.assertRaises(FileNotFoundError):
            file_.destination_directory = "./doesNotExist/"

    def test_destination_directory_is_file(self):
        """
        Should raise an exception.
        :return:
        """
        from artefact.localhost.file import FileCopy
        from businesslogic.errors import CollectorParameterError

        file_ = FileCopy(parameters={}, parent=None)
        with self.assertRaises(CollectorParameterError):
            file_.destination_directory = "./testfiles/test.txt"
