from __future__ import annotations

import logging
import os
from collections import namedtuple
from typing import List, Dict, Callable

import pandas as pd

from miner.data import FacebookData
from miner.utils import utils, const


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

    def _register_processors(self, preprocessor):
        preprocessor.register_command(utils.decode_data, utils.utf8_decoder)
        preprocessor.register_command(self._set_metadata)
        preprocessor.register_command(self._get_dataframe, field="messages")
        preprocessor.register_command(self._set_date_as_index, column="timestamp_ms")
        preprocessor.register_command(self._add_partner_column)
        preprocessor.register_command(self._split_media_column)
        return preprocessor

    def _set_metadata(self, data: Dict) -> Dict:
        data["thread_path"] = self._get_thread_path(data)
        data["media_dir"] = self._get_media_dir(data)
        data["participants"] = self._get_participants(data)

        _metadata = data.copy()
        del _metadata["messages"]

        metadata = namedtuple("metadata", sorted(_metadata))
        self._metadata = metadata(**_metadata)

        return data

    def _add_partner_column(self, data: pd.DataFrame) -> pd.DataFrame:
        data["partner"] = self._metadata.title
        return data

    def _get_thread_path(self, data: Dict) -> str:
        return self._get_dirname(data.get("thread_path"))

    def _get_media_dir(self, data: Dict) -> str:
        for message in data.get("messages"):
            if intersection := list(set(message) & set(const.MEDIA_DIRS)):
                uri = message.get(intersection[0])[0].get("uri")
                return self._get_dirname(os.path.dirname(os.path.dirname(uri)))

    @staticmethod
    def _get_participants(data: Dict) -> List[str]:
        return [participant.get("name") for participant in data.get("participants")]

    @staticmethod
    def _get_dirname(dirname: str) -> str:
        if "inbox/" in dirname:
            return dirname.split("inbox/")[1]
        elif "archived_threads/" in dirname:
            return dirname.split("archived_threads/")[1]
        else:
            logging.warning("WARNING! Missing thread_path for messages or media.")

    def _split_media_column(self, data: pd.DataFrame) -> pd.DataFrame:
        # TODO not yet used but can b
        # 2020-03-09 11:48:48.047,"[{'uri': 'messages/inbox/FooBar_n5fd6gG50h/audio/audioclip15905232600004598_2621787141481389.mp4', 'creation_timestamp': 1583750927}]"
        # if intersection := list(set(data) & set(const.MEDIA_DIRS)):
        #     media_cols = data.get(intersection)
        #     for col in media_cols:
        #         print(data[col])
        return data
