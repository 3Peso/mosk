from unittest import TestCase


class TestMosk(TestCase):
    def test_is_globalplaceholder_valid_filenotexistant(self):
        """Should return false"""
        from mosk import is_globalplaceholder_valid
        filepath = "doesnotexist.txt"

        self.assertFalse(is_globalplaceholder_valid(filepath))

    def test_is_globalplaceholder_valid_filexists(self):
        """Should return true"""
        from mosk import is_globalplaceholder_valid
        filepath = "test.txt"

        self.assertTrue(is_globalplaceholder_valid(filepath))
