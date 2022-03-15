import unittest
from pydantic import ValidationError
from bnotify.task import _find_bad_types, Task


class TestTask(unittest.TestCase):

    def test_task_order_right(self):
        def f(): pass
        token = "TOKEN STR"
        delay = 300

        task = Task(
            f,
            token,
            delay
        )
        self.assertEqual(task.function, f)
        self.assertEqual(task.token, token)
        self.assertEqual(task.delay, delay)

    def test_task_order_wrong(self):
        self.assertRaises(ValidationError, lambda: Task(
            "TOKEN STR",
            lambda a: a,
            300
        ))

    def test_task_less_args(self):
        self.assertRaises(TypeError, lambda: Task(
            lambda a: a,
            "TOKEN STR"
        ))


class TestTaskList(unittest.TestCase):

    def test_find_bad_types_empty(self):
        iterable = [tuple((1, 2, 3)), Task(lambda: 0, "TOKEN", 10)]

        bad_types = _find_bad_types(iterable)

        self.assertEqual(bad_types, [])

    def test_find_bad_types_filled(self):
        wrong_items = ['str', 1, 1.1, [1, 2, 3], {1, 2, 3}]
        wrong_types = [type(x) for x in wrong_items]
        iterable = [tuple((1, 2, 3)), Task(lambda: 0, "TOKEN", 10)] + wrong_items

        bad_types = _find_bad_types(iterable)

        self.assertEqual(bad_types, wrong_types)
