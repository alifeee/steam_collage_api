import steam_api
import unittest
import responses
# requests mocking: https://github.com/getsentry/responses
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


class TestGet64BitFromVanityUrl(unittest.TestCase):
    def setUp(self):
        self.baseurl = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
        self.baseparams = {
            "key": API_KEY,
        }

    @responses.activate
    def test_get64BitFromVanityUrl(self):
        params = self.baseparams.copy()
        params["vanityurl"] = "alifeee"
        responses.get(
            self.baseurl,
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
        params = self.baseparams.copy()
        params["vanityurl"] = "alifeee"
        responses.get(
            self.baseurl,
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
        params = self.baseparams.copy()
        params["vanityurl"] = ""
        responses.get(
            self.baseurl,
            match=[matchers.query_param_matcher(params)],
            status=400)
        self.assertRaises(
            Exception, steam_api.get64BitFromVanityUrl, "")


class TestGetGamesFromSteamId(unittest.TestCase):
    def setUp(self):
        self.baseurl = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
        self.baseparams = {
            "key": API_KEY,
            "format": "json",
            "include_appinfo": "true",
            "include_played_free_games": "true"
        }
        self.games = [
            {
                "appid": 10,
                "name": "Counter-Strike",
                "playtime_forever": 0,
                "img_icon_url": "2a9b1a1c8e8f9d1f9a9b1a1c8e8f9d1f9a9b1a1c",
                "playtime_windows_forever": 0,
                "playtime_mac_forever": 0,
                "playtime_linux_forever": 0,
                "rtime_last_played": 0,
            },
            {
                "appid": 20,
                "name": "Team Fortress Classic",
                "playtime_forever": 0,
                "img_icon_url": "2a9b1a1c8e8f9d1f9a9b1a1c8e8f9d1f9a9b1a1c",
                "playtime_windows_forever": 0,
                "playtime_mac_forever": 0,
                "playtime_linux_forever": 0,
                "rtime_last_played": 0,
            }
        ]

    @responses.activate
    def test_getGamesFromSteamId(self):
        params = self.baseparams.copy()
        params["steamid"] = "76561008099426919"
        responses.get(
            self.baseurl,
            match=[matchers.query_param_matcher(params)],
            json={
                "response": {
                    "game_count": 2,
                    "games": self.games
                }
            })
        games, game_count = steam_api.getGamesFromSteamId("76561008099426919")
        self.assertEqual(games, self.games)
        self.assertEqual(game_count, 2)

    @responses.activate
    def test_emptyQuery(self):
        params = self.baseparams.copy()
        params["steamid"] = ""
        responses.get(
            self.baseurl,
            match=[matchers.query_param_matcher(params)],
            status=500)
        self.assertRaises(
            Exception, steam_api.getGamesFromSteamId, "")

    @responses.activate
    def test_invalidSteamId(self):
        params = self.baseparams.copy()
        params["steamid"] = "invalid"
        responses.get(
            self.baseurl,
            match=[matchers.query_param_matcher(params)],
            status=500)
        self.assertRaises(
            Exception, steam_api.getGamesFromSteamId, "invalid")


class TestGetImageUrlForGameId(unittest.TestCase):
    def setUp(self):
        self.baseurl = "https://cdn.cloudflare.steamstatic.com/steam/apps/{game_id}/header.jpg"

    def test_getImageUrlForGameId(self):
        game_id = 10
        self.assertEqual(
            steam_api.getImageUrlForGameId(game_id),
            self.baseurl.format(game_id=game_id))

    def test_getImageUrlForGameId2(self):
        game_id = 205560
        self.assertEqual(
            steam_api.getImageUrlForGameId(game_id),
            self.baseurl.format(game_id=game_id))
