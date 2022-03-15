import unittest
from bnotify import BotNotifier, TaskList, Task


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

    def test_tasks_serve(self):
        app = BotNotifier()
        delay = 100
        token = 'TOKEN'

        @app.serve(token, delay)
        def sample_function():
            pass

        self.assertEqual(app.tasks, TaskList(
            Task(sample_function, token, delay)
        ))

    def test_tasks_serve_several(self):
        app = BotNotifier()
        delay = 100
        token = 'TOKEN'

        @app.serve(token, delay)
        def sample_function_1():
            pass

        @app.serve(token, delay)
        def sample_function_2():
            pass

        self.assertEqual(app.tasks, TaskList([
            Task(sample_function_1, token, delay),
            Task(sample_function_2, token, delay)
        ]))

    def test_tasks_addition(self):
        app = BotNotifier()
        delay = 100
        token = 'TOKEN'

        def sample_function():
            pass

        app.tasks += (sample_function, token, delay)

        self.assertEqual(app.tasks, TaskList(
            Task(sample_function, token, delay)
        ))
