# -*- coding: utf-8 -*-

"""
    bnotify
    ~~~

    An out-of-the-box telagram bot notification sender.

    :copyright: (c) 2022 by Stepan Starovoitov.
    :license: BSD, see LICENSE for more details.
"""
__version__ = "0.0.1"

from typing import Optional, Callable
from pymongo import MongoClient

from bnotify.task import TaskList, TaskThread, Task
from bnotify.telegram import Message, DocumentMessage, Document

Message = Message
Document = Document
DocumentMessage = DocumentMessage

class BotNotifier:
    """
    The main bnotify object. On initialization it will load empty parameter
    tasks: TaskList, which should be later filled with Task objects.
    The BotNotifier is launched by executing the code below::

        app = BotNotifier()
        app.tasks += Task(task_func_1, 600, TOKEN)
        app.run()

    task_func_1 will be filled with db: MongoClient parameter, if mongo_url and db_name parameters are filled.

    :param mongo_url: string "mongodb://HOST:PORT/" specifying connection to mongodb
                    may also include any parameters that can be specified in mongodb connection protocol
    :param db_name: database name

    """
    tasks: TaskList = None

    def __init__(self,
                 mongo_url: str = '',
                 db_name: str = ''
                 ):
        self.tasks = TaskList()
        self.mongo_url = mongo_url
        self.db_name = db_name

    def _has_db(self) -> bool:
        """
        Returns True if mongo_url and db_name are filled.
        """
        return bool(self.mongo_url) and bool(self.db_name)

    def _new_connection_to_db(self) -> Optional[MongoClient]:
        """
        Creates new connection to db if instance have mongo_url and db_name filled.

        :return: MongoClient or None
        """
        if self._has_db():
            return MongoClient(self.mongo_url)[self.db_name]
        else:
            return None

    def serve(self, token: str, delay: int = 600) -> Callable:
        def wrapper(func: Callable) -> Callable:
            self.tasks += Task(func, token, delay)
            return func
        return wrapper

    def run(self) -> None:
        """
        Using threads (not processes or async) because speed is not important.
        Most of the time tasks should be asleep.

        :return: None
        """
        threads = []
        for task in self.tasks:
            # if isinstance(task, Task):
            #     task_thread = TaskThread(**task, db=self._new_connection_to_db())
            task_thread = TaskThread(task, db=self._new_connection_to_db())
            task_thread.start()

        for thread in threads:
            thread.join()
