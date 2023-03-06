import steam_api
import unittest

class TestIsVanityUrl(unittest.TestCase):
    def test_vanityUrl(self):
        self.assertTrue(steam_api.isVanityUrl("alifeee"))

    def test_vanityUrl2(self):
        self.assertTrue(steam_api.isVanityUrl("123456789"))

    def test_64biturl(self):
        self.assertFalse(steam_api.isVanityUrl("76561198099426919"))

