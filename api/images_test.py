import images
import unittest
import responses
from PIL import Image
from parameterized import parameterized


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


test_image_folder = "api/test_images/"
game_ids = [
    "440",
    "207140",
    "213650",
    "226100",
    "247000",
]
game_images = [
    Image.open(test_image_folder + game_id + ".jpg")
    for game_id in game_ids
]


class TestBytesFromPilImage(unittest.TestCase):
    def test_bytesFromPilImage(self):
        self.skipTest("Not implemented yet")


class TestGetImageForGameId(unittest.TestCase):
    @parameterized.expand(zip(game_ids, game_images))
    def test_getImageForGameId(self, game_id, expected_image):
        for image, id in zip(game_images, game_ids):
            responses.add(
                responses.GET,
                images.getImageUrlForGameId(id),
                body=image.tobytes(),
                status=200,
                content_type="image/jpeg",
            )
        img = images.getImageForGameId(game_id)
        self.assertEqual(img, expected_image)
