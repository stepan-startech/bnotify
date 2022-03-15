import unittest
from bnotify import BotNotifier


class TestBotNotifier(unittest.TestCase):

    def test_has_db_true(self):
        app = BotNotifier(
            mongo_url="mongodb://localhost:27017",
            db_name="some_db"
        )
        self.assertTrue(app._has_db())

    def test_has_db_none_false(self):
        app = BotNotifier()
        self.assertFalse(app._has_db())

    def test_has_db_url_false(self):
        app = BotNotifier(
            mongo_url="mongodb://localhost:27017"
        )
        self.assertFalse(app._has_db())

    def test_has_db_db_false(self):
        app = BotNotifier(
            db_name="some_db"
        )
        self.assertFalse(app._has_db())
