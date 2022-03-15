# -*- coding: utf-8 -*-

"""
    Mongodb based notifications
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This example shows basic usage of bnotify, initialised with a database.
    Telegram has no "find all users" method in api, so it is reasonable to save users chat_id on their requests.
    As this is not a fully functional telegram api client, described action should be done by another module.

    Checkout Bnotify at https://github.com/startech-live/bnotify

    This snippet by Stepan Starovoitov can be used freely for anything you like.
    Consider it public domain.
"""
from bnotify import BotNotifier
from bnotify.telegram import Message, DocumentMessage, Document
from pymongo import MongoClient
TOKEN = ""


app = BotNotifier(
    mongo_url="mongodb://localhost:27017",
    db_name="test_bnotify"
)


def get_users(db: MongoClient):
    return [user["chat_id"] for user in db["user"].find_many({}, {"chat_id": 1})]


@app.serve(TOKEN, 100)
def test_message(db: MongoClient):
    for user in get_users(db):
        yield Message(
            text="Hello there!",
            chat_id=user
        )


@app.serve(TOKEN, 100)
def test_document(db: MongoClient):
    for user in get_users(db):
        yield DocumentMessage(
            text="Hello there!",
            chat_id=user,
            document=Document(
                name="Filename.txt",
                content=b"Test file"
            )
        )


if __name__ == "__main__":
    app.run()
