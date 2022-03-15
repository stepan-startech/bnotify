from dataclasses import dataclass
from io import BytesIO
from typing import Union

import requests

from bnotify.log import logger


@dataclass(frozen=True)
class Message:
    """
    Special datatype containing data necessary to send a text message to a user.
    """
    text: str
    chat_id: int


@dataclass(frozen=True)
class Document:
    """
    Special datatype containing data necessary to send a document to a user.
    """
    name: str
    content: bytes


@dataclass(frozen=True)
class DocumentMessage:
    """
    Special datatype containing data necessary to send a text message with a document to a user.
    """
    chat_id: int
    document: Document
    text: str = ""


def _process_request(response: requests.Response):
    if response.status_code // 100 == 2:
        logger.info(f"Response {response.status_code} {response.text}")
    else:
        logger.error(f"Response {response.status_code} {response.raw}")


TG_BOT_URL = "https://api.telegram.org/bot{}/{}"


class TelegramBotApi:
    def __init__(self, token: str):
        self.token = token

    def _form_text_message(self, message: Message):
        request_args = {
            "url": TG_BOT_URL.format(self.token, "sendMessage"),
            "data": {
                "chat_id": message.chat_id,
                "text": message.text
            }
        }
        return request_args

    def _form_document(self, message: DocumentMessage):
        data = {
            "chat_id": message.chat_id
        }
        if message.text:
            data["caption"] = message.text

        file_obj = BytesIO(message.document.content)
        file_obj.name = message.document.name

        request_args = {
            "url": TG_BOT_URL.format(self.token, "sendDocument"),
            "data": data,
            "files": {"document": file_obj}
        }
        return request_args

    def send_message(self, message: Message):
        result = requests.post(**self._form_text_message(message))
        _process_request(result)

    def send_document(self, message: DocumentMessage):
        result = requests.post(**self._form_document(message))
        _process_request(result)