import steam_api
import unittest
import responses
from responses import matchers

with open("api_key.txt", "r") as f:
    API_KEY = f.read()


class TestIsVanityUrl(unittest.TestCase):
    def test_vanityUrl(self):
        self.assertTrue(steam_api.isVanityUrl("alifeee"))

    def test_vanityUrl2(self):
        self.assertTrue(steam_api.isVanityUrl("123456789"))

    def test_64biturl(self):
        self.assertFalse(steam_api.isVanityUrl("76561198099426919"))


baseurl = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
baseparams = {
    "key": API_KEY,
}


class TestGet64BitFromVanityUrl(unittest.TestCase):
    @responses.activate
    def test_get64BitFromVanityUrl(self):
        params = baseparams.copy()
        params["vanityurl"] = "alifeee"
        responses.get(
            baseurl,
            match=[matchers.query_param_matcher(params)],
            json={
                "response": {
                    "steamid": "76561008099426919",
                    "success": 1
                }
            })
        self.assertEqual(steam_api.get64BitFromVanityUrl(
            "alifeee"), "76561008099426919")

    @responses.activate
    def test_nonExistentUrl(self):
        params = baseparams.copy()
        params["vanityurl"] = "alifeee"
        responses.get(
            baseurl,
            match=[matchers.query_param_matcher(params)],
            json={
                "response": {
                    "success": 42,
                    "message": "No match"
                }
            })
        self.assertRaises(
            Exception, steam_api.get64BitFromVanityUrl, "alifeee")

    @responses.activate
    def test_emptyQuery(self):
        params = baseparams.copy()
        params["vanityurl"] = ""
        # returns <html><head><title>Bad Request</title></head><body><h1>Bad Request</h1>Required
        # parameter 'vanityurl' is missing</body></html>
        responses.get(
            baseurl,
            match=[matchers.query_param_matcher(params)],
            status=400)
        self.assertRaises(
            Exception, steam_api.get64BitFromVanityUrl, "")
