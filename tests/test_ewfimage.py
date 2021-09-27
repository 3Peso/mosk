import platform
import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestEWFImageDunderInit(TestCase):
    @unittest.skipIf(platform.system() == "Windows", "Platform currently not supported.")
    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test___init__image_info(self):
        """
        Should initialize member _imageInfo with EwfImageInfo object.
        :return:
        """
        import pyewf
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            actual_ewf_image = EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        self.assertEqual(expected_image_info, actual_ewf_image._imageinfo)

    @unittest.skipIf(platform.system() == "Windows", "Platform currently not supported.")
    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test___init__initialize_partition_lookup(self):
        """
        Should call _initialize_partition_lookup
        :return:
        """
        import pyewf
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        init_mock = MagicMock(return_value=None)
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            with patch('source.ewfimage.EWFImage._initialize_partition_lookup', init_mock):
                EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        init_mock.assert_called_once()

    @unittest.skipIf(platform.system() == "Windows", "Platform currently not supported.")
    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test___init__filesysteminfo(self):
        """
        Should initialize member _filesysteminfo as empty dict.
        :return:
        """
        import pyewf
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_filesysteminfo: dict = {}
        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            actual_ewf_image = EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        self.assertEqual(expected_filesysteminfo, actual_ewf_image._filesysteminfo)

    @unittest.skipIf(platform.system() == "Windows", "Platform currently not supported.")
    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test___init__fs_discovered(self):
        """
        Should initialize member _fs_discoverd with False
        :return:
        """
        import pyewf
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_fs_discovered: bool = False
        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            actual_ewf_image = EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        self.assertEqual(expected_fs_discovered, actual_ewf_image._fs_discoverd)

    @unittest.skipIf(platform.system() == "Windows", "Platform currently not supported.")
    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=True))
    def test___init__discover_parameter_true(self):
        """
        Should initialize member _fs_discoverd with True and call _initialize_partitions.
        :return:
        """
        import pyewf
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_fs_discovered: bool = True
        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        init_mock = MagicMock(return_value=None)
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            with patch('source.ewfimage.EWFImage._initialize_partitions', init_mock):
                actual_ewf_image = EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        self.assertEqual(expected_fs_discovered, actual_ewf_image._fs_discoverd)
        init_mock.assert_called_once()

    @unittest.skipIf(platform.system() == "Windows", "Platform currently not supported.")
    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test___init__discover_parameter_false(self):
        """
        Should not call _initialize_partitions.
        :return:
        """
        import pyewf
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        init_mock = MagicMock(return_value=None)
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            with patch('source.ewfimage.EWFImage._initialize_partitions', init_mock):
                EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        init_mock.assert_not_called()


class TestEWFImage(TestCase):
    @unittest.skipIf(platform.system() == "Windows", "Platform currently not supported.")
    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test_filesysteminfo_discover_not_set(self):
        """
        Should raise an error
        :return:
        """
        import pyewf
        from source.ewfimage import EWFImage, EWFImageInfo
        from businesslogic.errors import CollectorParameterError

        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            ewf_image = EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})
            with self.assertRaises(CollectorParameterError):
                ewf_image.filesysteminfo


class TestEWFPartitionFSObjectGetter(TestCase):
    def test_fs_object(self):
        """Should raise LookupError if _fs_object is none"""
        from source.ewfimage import EWFPartition

        partition = EWFPartition(fs_object=None, partition={})

        with self.assertRaises(LookupError):
            partition.fs_object
