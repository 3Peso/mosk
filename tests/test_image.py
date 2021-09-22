from unittest import TestCase, mock
from unittest.mock import MagicMock

from businesslogic.errors import ImageFileError


class TestImage(TestCase):
    @mock.patch('source.baseclasses.image.Image.__init__', MagicMock(return_value=None))
    def test_imagefilepath_setter(self):
        """
        Should set the member _imagefilepath
        Should set the member _imagetype
        :return:
        """
        from source.baseclasses.image import Image
        from source.baseclasses.image import ImageType

        expected_image_file = "dummy.e01"
        expected_image_file_type = ImageType(Type='ewf', FileEnding='.e01')
        image = Image()
        with mock.patch('source.baseclasses.image.os.path.exists', MagicMock(return_value=True)):
            image.imagefilepath = expected_image_file

        self.assertEqual(expected_image_file, image._imagefilepath)
        self.assertEqual(expected_image_file_type, image._imagetype)

    @mock.patch('source.baseclasses.image.Image.__init__', MagicMock(return_value=None))
    def test_imagefilepath_setter_file_not_ewf(self):
        """
        Should raise an ImageFileError
        :return:
        """
        from source.baseclasses.image import Image

        expected_image_file = "dummy.aff"
        image = Image()
        with mock.patch('source.baseclasses.image.os.path.exists', MagicMock(return_value=True)):
            with self.assertRaises(ImageFileError):
                image.imagefilepath = expected_image_file

    @mock.patch('source.baseclasses.image.Image.__init__', MagicMock(return_value=None))
    def test_imagefilepath_setter_file_not_found(self):
        """
        Should raise a FileNotFoundError
        :return:
        """
        from source.baseclasses.image import Image

        expected_image_file = "dummy.e01"
        image = Image()
        with self.assertRaises(FileNotFoundError):
            image.imagefilepath = expected_image_file
