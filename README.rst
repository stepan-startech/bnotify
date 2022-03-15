bnotify
====
.. image:: https://img.shields.io/badge/test-pass-00d200.svg
    :target: nono

.. image:: https://img.shields.io/badge/build-pass-00d200.svg
    :target: nono

.. image:: https://img.shields.io/badge/license-BSD-blue.svg?style=flat-square
    :target: https://en.wikipedia.org/wiki/BSD_License

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

Bnotify is an open source Python telegram bots notifications module designed for humans. It
allows to provide regular notifications to your telegram bot. Bnotify offers native support for MongoDB.

How to install
-------------

.. code-block:: bash

    python3 setup.py install --user


Bnotify is Simple
-------------
.. code-block:: python

    from bnotify import BotNotifier, Message

    def send_hi():
        yield Message(
                text="Hi",
                chat_id=0000000
            )

    app = BotNotifier()

    app.tasks += (send_hi, 100, "TELEGRAM_TOKEN")

    app.run()

Tasks are now alive and ready to send messages.

To make notifications more functional, you can connect to your API or database to retrieve users information.
Make sure that the way you use data storages is thread-safe.
Bnotify comes with native thread-safe support for mongodb:

.. code-block:: python

    from bnotify import BotNotifier, Message
    from mongo import MongoClient

    def send_hi(db: MongoClient):
        for user in db.user.find({}, {"chat_id":1}):
            yield Message(
                    text="Hi",
                    chat_id=user["chat_id"]
                )

    app = BotNotifier(
        mongo_url="mongodb://localhost:27017",
        db_name="sample_db"
    )

    app.tasks += (send_hi, 100, "TELEGRAM_TOKEN")

    app.run()




`Check out the Bnotify Website <https://bnotify.startech.live/>`_

Features
--------
* Parallel tasks
* Enhanced Logging
* Operations Log
* MongoDB Support

License
-------
Bnotify is a `Stepan Starovoitov`_ open source project,
distributed under the `BSD license
<https://github.com/startech-live/bnotify/blob/master/LICENSE>`_.

.. _`Stepan Starovoitov`: https://starovoitov.startech.live
