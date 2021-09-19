import pyewf
from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestEWFImageDunderInit(TestCase):
    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test___init__image_info(self):
        """
        Should initialize member _imageInfo with EwfImageInfo object.
        :return:
        """
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            actual_ewf_image = EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        self.assertEqual(expected_image_info, actual_ewf_image._imageinfo)

    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test___init__initialize_partition_lookup(self):
        """
        Should call _initialize_partition_lookup
        :return:
        """
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        init_mock = MagicMock(return_value=None)
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            with patch('source.ewfimage.EWFImage._initialize_partition_lookup', init_mock):
                EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        init_mock.assert_called_once()

    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test___init__filesysteminfo(self):
        """
        Should initialize member _filesysteminfo as empty dict.
        :return:
        """
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_filesysteminfo: dict = {}
        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            actual_ewf_image = EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        self.assertEqual(expected_filesysteminfo, actual_ewf_image._filesysteminfo)

    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test___init__fs_discovered(self):
        """
        Should initialize member _fs_discoverd with False
        :return:
        """
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_fs_discovered: bool = False
        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            actual_ewf_image = EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        self.assertEqual(expected_fs_discovered, actual_ewf_image._fs_discoverd)

    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=True))
    def test___init__discover_parameter_true(self):
        """
        Should initialize member _fs_discoverd with True and call _initialize_partitions.
        :return:
        """
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_fs_discovered: bool = True
        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        init_mock = MagicMock(return_value=None)
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            with patch('source.ewfimage.EWFImage._initialize_partitions', init_mock):
                actual_ewf_image = EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        self.assertEqual(expected_fs_discovered, actual_ewf_image._fs_discoverd)
        init_mock.assert_called_once()

    @patch('source.ewfimage.os.path.exists', MagicMock(return_value=True))
    @patch('source.ewfimage.EWFImage._initialize_partition_lookup', MagicMock(return_value=None))
    @patch('businesslogic.placeholders.Placeholder.replace_placeholders', MagicMock(return_value='test.e01'))
    @patch('source.ewfimage.str_to_bool', MagicMock(return_value=False))
    def test___init__discover_parameter_false(self):
        """
        Should not call _initialize_partitions.
        :return:
        """
        from source.ewfimage import EWFImage, EWFImageInfo

        expected_image_info: EWFImageInfo = EWFImageInfo(ewf_handle=pyewf.handle())
        init_mock = MagicMock(return_value=None)
        with patch('source.ewfimage.EWFImage._get_image_information', MagicMock(return_value=expected_image_info)):
            with patch('source.ewfimage.EWFImage._initialize_partitions', init_mock):
                EWFImage(parent=None, parameters={'filepath': 'test.e01', 'discover': False})

        init_mock.assert_not_called()
