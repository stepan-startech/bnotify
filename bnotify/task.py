from dataclasses import dataclass
from threading import Thread
from time import sleep
from typing import Callable, Union

from bnotify.telegram import TelegramBotApi, Message, DocumentMessage, Document


@dataclass(frozen=True)
class Task:
    """
    Dataclass containing task function and several properties, such as
    - delay: pause in seconds between function runs
    - token: telegram bot token
    Token is specified for each task to give additional flexibility: one notifier instance may serve several bots.

    Function will be filled with db: MongoClient parameter, if mongodb is connected.
    """
    function: Callable
    token: str
    delay: int


def _find_bad_types(iterable: list) -> list:
    """
    Function find types incompatible with TaskList class within iterable.
    """
    return [type(x) for x in iterable if not isinstance(x, tuple) and not isinstance(x, Task)]


class TaskList(list):
    """
    Special type made for storing BotNotifier tasks based on list type.
    Tasks are organized in format [(),(),()] or [Task(),Task(),Task()], which allows adding and removing tasks,
    but forbidden their modification.
    """
    def __init__(self, content: Union[list, tuple, Task] = None):
        """
        This class supports initialization with a list of tuples, or a tuple.
        Tuple will be converted to a list containing tuple.

        :param content: list or tuple to initialize TaskList with
        """
        if not content:
            content = []
        if isinstance(content, list):
            bad_types = _find_bad_types(content)
            if bad_types:
                raise TypeError(
                    f'can only initialize TaskList with list of tuples or tuple (not "{bad_types}") ')
        elif isinstance(content, tuple) or isinstance(content, Task):
            content = [content]
        else:
            raise TypeError(
                f'can only initialize TaskList with list of tuples or tuple (not "{type(content)}") ')
        super(TaskList, self).__init__(content)

    def _default_concatenation(self, other):
        """
        This class supports tuple and list additions.
        Basically two behaviours defined:
         - tuple appends to a new instance of TaskList,
         - list of tuples extends it,
         all done along with old TaskList content.
         Other objects ore not supported.

        :param other: object to concatenate with
        :return: new object as a result of concatenation
        """
        if isinstance(other, list):
            not_tuple = _find_bad_types(other)
            if not not_tuple:
                new = TaskList()
                new.extend(self)
                other = [Task(*o) if type(o) != Task else o for o in other]
                new.extend(other)
                return new
            else:
                raise TypeError(
                    f'can only concatenate list of tuples (extend) or tuple (append) with TaskList obj (not "{not_tuple}") ')
        elif isinstance(other, tuple):
            new = TaskList()
            new.extend(self)
            new.append(Task(*other))
            return new
        elif isinstance(other, Task):
            new = TaskList()
            new.extend(self)
            new.append(other)
            return new
        else:
            raise TypeError(f'can only concatenate list of tuples (extend) or tuple (append) with TaskList obj (not "{type(other)}") ')

    def __add__(self, other):
        """
        This class supports tuple and list additions.
        Basically two behaviours defined:
         - tuple appends to a new instance of TaskList,
         - list of tuples extends it,
         all done along with old TaskList content.
         Other objects ore not supported.

        :param other: object to concatenate with
        :return: new object as a result of concatenation
        """
        return self._default_concatenation(other)

    def __iadd__(self, other):
        """
        This class supports tuple and list additions.
        Basically two behaviours defined:
         - tuple appends to a new instance of TaskList,
         - list of tuples extends it,
         all done along with old TaskList content.
         Other objects ore not supported.

        :param other: object to concatenate with
        :return: new object as a result of concatenation
        """
        return self._default_concatenation(other)


class TaskThread(Thread):

    def __init__(self, task: Task, db=None):
        self.task = task
        self.db = db
        self.tg_client = TelegramBotApi(self.task.token)
        super(TaskThread, self).__init__()

    def _send_message(self, message):
        if isinstance(message, Message):
            self.tg_client.send_message(message)
        elif isinstance(message, DocumentMessage):
            self.tg_client.send_document(message)
        elif isinstance(message, Document):
            pass

    def run(self):
        while True:
            if self.db:
                task_messages = self.task.function(self.db)
            else:
                task_messages = self.task.function()

            for message in task_messages:
                self._send_message(message)

            sleep(self.task.delay)

