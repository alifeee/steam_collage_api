import images
import unittest


class TestGetImageUrlForGameId(unittest.TestCase):
    def setUp(self):
        self.baseurl = "https://cdn.cloudflare.steamstatic.com/steam/apps/{game_id}/header.jpg"

    def test_getImageUrlForGameId(self):
        game_id = 10
        self.assertEqual(
            images.getImageUrlForGameId(game_id),
            self.baseurl.format(game_id=game_id))

    def test_getImageUrlForGameId2(self):
        game_id = 205560
        self.assertEqual(
            images.getImageUrlForGameId(game_id),
            self.baseurl.format(game_id=game_id))
