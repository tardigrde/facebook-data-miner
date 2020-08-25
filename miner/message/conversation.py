from __future__ import annotations

from typing import Union, List, Dict, Callable, Any
from collections import namedtuple
import pandas as pd
import os

from miner.data import FacebookData
from miner import utils


class Conversation(FacebookData):
    """
    Class for representing data of all the messages with a user or a group
    """

    def __init__(
        self, path: str, reader: Callable = None, processors: List[Callable] = None
    ) -> None:
        super().__init__(path, reader=reader, processors=processors)

    def __add__(self, other: Conversation):
        self.data = pd.concat([self.data, other.data]).sort_index()
        return self

    def register_processors(self, preprocessor):
        preprocessor.register_command(utils.decode_data, utils.utf8_decoder)
        preprocessor.register_command(self.set_metadata)
        preprocessor.register_command(self.get_dataframe, field="messages")
        preprocessor.register_command(self.set_date_as_index, column="timestamp_ms")
        preprocessor.register_command(self.add_partner_column)
        return preprocessor

    def set_metadata(self, data: Dict) -> Dict:
        data["thread_path"] = self.get_thread_path(data)
        data["media_dir"] = self.get_media_dir(data)
        data["participants"] = self.get_participants(data)

        _metadata = data.copy()
        del _metadata["messages"]

        metadata = namedtuple("metadata", sorted(_metadata))
        self._metadata = metadata(**_metadata)

        return data

    def add_partner_column(self, data: pd.DataFrame) -> pd.DataFrame:
        data["partner"] = self._metadata.title
        return data

    def get_thread_path(self, data: Dict) -> str:
        return self.get_dirname(data.get("thread_path"))

    def get_media_dir(self, data: Dict) -> str:
        for message in data.get("messages"):
            if intersection := list(set(message) & set(utils.MEDIA_DIRS)):
                uri = message.get(intersection[0])[0].get("uri")
                return self.get_dirname(os.path.dirname(os.path.dirname(uri)))

    @staticmethod
    def get_participants(data: Dict) -> List[str]:
        return [participant.get("name") for participant in data.get("participants")]

    @staticmethod
    def get_dirname(dirname: str) -> str:
        if "inbox/" in dirname:
            return dirname.split("inbox/")[1]
        elif "archived_threads/" in dirname:
            return dirname.split("archived_threads/")[1]
        else:
            print("WARNING! Missing thread_path for messages or media.")
