# -*- coding: utf-8 -*-

"""
    Basic notifications.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This example shows basic usage of bnotify.
    To start using bnotify, define the application first,
    then attach a function which returns or "yields" a list of message objects.
    You will need to provide telegram chat id with each message.


    Checkout Bnotify at https://github.com/startech-live/bnotify

    This snippet by Stepan Starovoitov can be used freely for anything you like.
    Consider it public domain.
"""
import sys

from bnotify import BotNotifier
from bnotify.telegram import Message, DocumentMessage, Document
import config

TOKEN = config.TOKEN
CHAT_IDS = config.USERS


app = BotNotifier()


@app.serve(TOKEN, 10)
def test_message():
    for user in CHAT_IDS:
        yield Message(
            text="Do not forget to take your pills!",
            chat_id=user
        )


@app.serve(TOKEN, 10)
def test_document():
    for user in CHAT_IDS:
        yield DocumentMessage(
            text="Your daily news!",
            chat_id=user,
            document=Document(
                name="News.txt",
                content=b"Stop R/U conflict!\n\nShocking news! Pu*in is a fa**ot!"
            )
        )


if __name__ == "__main__":
    app.run()
