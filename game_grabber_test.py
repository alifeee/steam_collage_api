import game_grabber
import unittest


def decimalUrl(id, sort): return "https://steamcommunity.com/profiles/" + \
    id+"/games/?tab=all&sort="+sort


def customUrl(id, sort): return "https://steamcommunity.com/id/" + \
    id+"/games/?tab=all&sort="+sort


class TestGetUrl(unittest.TestCase):
    def test_url(self):
        id = "alifeee"
        url = customUrl(id, "playtime")

        self.assertEqual(game_grabber._getProfileUrl(id), url)

    def test_decimalUrl(self):
        id = "123456789"
        url = decimalUrl(id, "playtime")

        self.assertEqual(game_grabber._getProfileUrl(id), url)

    def test_nameSorting(self):
        id = "alifeee"
        url = customUrl(id, "name")

        self.assertEqual(game_grabber._getProfileUrl(id, "name"), url)

    def test_playtimeSorting(self):
        id = "alifeee"
        url = customUrl(id, "playtime")

        self.assertEqual(game_grabber._getProfileUrl(id, "playtime"), url)

    def test_achievementsSorting(self):
        id = "alifeee"
        url = customUrl(id, "achievements")

        self.assertEqual(game_grabber._getProfileUrl(id, "achievements"), url)

    def test_invalidSorting(self):
        id = "alifeee"
        with self.assertRaises(AssertionError):
            game_grabber._getProfileUrl(id, "invalid")


class TestHTMLParser(unittest.TestCase):
    def setUp(self):
        self.html = """
        <div id="games_list_row_container">
        <div id="games_list_rows">
        <div id="game_105600" class="gameListRow">Terraria</div>
        <div id="game_440" class="gameListRow">TF2</div>
        <div id="game_252950" class="gameListRow">Rocket League</div>
        </div>
        </div>
        """

    def test_getGamesFromHTML(self):
        games = game_grabber._getGamesFromHTML(self.html)
        self.assertEqual(len(games), 3)
        self.assertEqual(games[0], "105600")
        self.assertEqual(games[1], "440")
        self.assertEqual(games[2], "252950")
