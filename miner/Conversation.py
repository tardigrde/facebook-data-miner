from typing import Union, List, Dict, Callable, Any
from datetime import datetime
import pandas as pd
import os

from miner.FacebookData import FacebookData
from miner import utils

from collections import namedtuple


class Conversation(FacebookData):
    """
    Class for representing data of all the messages with a user or a group
    """

    def __init__(self, path: str, reader: Callable = None, processors: List[Callable] = None) -> None:
        self.path: str = path
        self._reader: Callable = reader
        self._processors: List[Callable] = processors

        super().__init__()

    @property
    def reader(self) -> Callable:
        return self._reader if self._reader is not None else utils.read_json

    @property
    def processors(self) -> List[Callable]:
        if self._processors is not None:
            return self._processors
        return [
            self.decode_text, self.separate_metadata, self.get_dataframe,
            self.set_date_as_index, self.add_partner_column
        ]

    def separate_metadata(self, data: Dict) -> List:
        # NOTE this changes state: self._metadata

        # TODO media_dir not needed now; takes a long time to iterate over all the messages
        # can be filtered later for df
        # on the other hand would be nice to have the media_dir in the metadata

        data['thread_path'] = self.get_thread_path(data)
        data['media_dir'] = self.get_media_dir(data)

        messages = data.get('messages')
        del data['messages']

        metadata = namedtuple('metadata', sorted(data))
        self._metadata = metadata(**data)

        return messages

    def add_partner_column(self, data: pd.DataFrame) -> pd.DataFrame:
        data['partner'] = self._metadata.title
        return data

    @staticmethod
    def set_date_as_index(data: pd.DataFrame) -> pd.DataFrame:
        date_series = data.timestamp_ms.apply(utils.ts_to_date)
        return data.set_index(date_series).iloc[::-1]

    @staticmethod
    def get_thread_path(data: Dict) -> str:
        thread_path = data.get('thread_path')
        if thread_path.startswith('inbox/'):
            return thread_path.split('inbox/')[1]
        elif thread_path.startswith('archived_threads/'):
            return thread_path.split('archived_threads/')[1]
        else:
            raise ValueError('Field `thread_path` should start with `inbox/` or `archived_threads/`.')



    @staticmethod
    def get_media_dir(data: Dict) -> str:  # TODO simplify
        for message in data.get('messages'):
            intersected_keys = list(set(message) & set(utils.MEDIA_DIRS))
            if intersected_keys:
                uri = message.get(intersected_keys[0])[0].get('uri')
                if uri not in utils.MEDIA_DIRS:
                    continue
                try:
                    return os.path.dirname(os.path.dirname(uri)).split('inbox/')[1]
                except IndexError:
                    print('Uri was ', uri)

        # NOTE this is the df version of getting the media_dir if needed
        # for media in utils.MEDIA_DIRS:
        #     if media in self._df.columns:
        #         media_in_msg = list(self._df[media][self._df[media].notnull()])
        #         uri = media_in_msg[0][0].get('uri')
        #         return os.path.dirname(os.path.dirname(uri)).split('inbox/')[1]

# class Conversation:
#     """
#     Class for representing data of all the messages with a user or a group
#     """
#
#     # TODO THIS class should be named Conversation
#     # TODO make messages iterable?!
#
#     def __init__(self, json_path):
#         super().__init__(json_path)
#         # TODO THESE are all fujnctions that can be put in a pipeline. this and this and this has to happen with the msg df
#         # as part of preprocess?!
#         self.to_df('messages') # TODO Messages.df is a misleading abstraction. Convo.messages is a good
#         self.set_date_as_index()
#         self.add_partner_column()
#
#     @property
#     def names(self):
#         # TODO names? bad name?! name vs participants
#         # TODO symetricallity should be kept with Friends and all tabular data
#         try:
#             return pd.DataFrame(self.participants)[0]
#         except KeyError:
#             return pd.Series({0: 'Facebook User'})
#
#     @property
#     def participants(self):
#         # TODO p
#         participants = self.decoded.get('participants')
#         return [p.get('name') for p in participants if p.get('name')]
#
#     @property
#     def title(self):
#         return self.decoded.get('title')
#
#     @property
#     def ttype(self):
#         # TODO name bad
#         return self.decoded.get('thread_type')
#
#     @property
#     def messages_dir(self):
#         # TODO json dir
#         thread_path = self.decoded.get('thread_path')
#         if not thread_path.startswith('inbox/'):
#             raise ValueError('Field `thread_path` should start with `inbox/`.')
#         return thread_path.split('inbox/')[1]
#
#     @property
#     def media_dir(self):
#         # TODO name should be ok
#         for media in utils.MEDIA_DIRS:
#             if media in self._df.columns:
#                 media_in_msg = list(self._df[media][self._df[media].notnull()])
#                 uri = media_in_msg[0][0].get('uri')
#                 return os.path.dirname(os.path.dirname(uri)).split('inbox/')[1]
#
#     def set_date_as_index(self):
#         date_series = self._df.timestamp_ms.apply(self.ts_to_date)
#         self._df = self._df.set_index(date_series).iloc[::-1]
#
#     def add_partner_column(self):
#         self._df['partner'] = self.title
#
#     @staticmethod
#     def ts_to_date(date):
#         return datetime.fromtimestamp(date / 1000)
