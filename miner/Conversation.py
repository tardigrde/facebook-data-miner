from typing import Union, List, Dict, Callable, Any
from datetime import datetime
import pandas as pd
import os

from miner.FacebookData import TabularFacebookData, FacebookData
from miner import utils


class Conversation:
    sub_path = '/messages/inbox'
    """
    Class for representing data of all the messages with a user or a group
    """

    # TODO THIS class should be named Conversation
    # TODO make messages iterable?!

    def __init__(self, path: str, msgs_dir: str = '', reader: Callable = None,
                 processors: List[Callable] = None) -> None:
        self.path = self.make_path(path, additional=msgs_dir)
        self._reader = reader
        self._processors = processors

        fb = FacebookData(self.path)
        self._data = fb.get_data(reader=self.reader, processors=self.processors)

    def make_path(self, path, additional: str = ''):
        return path + self.sub_path + additional

    @property
    def reader(self):
        return utils.read_json

    @property
    def processors(self) -> Any:
        # TODO maybe a better solution for passing in args and kwargs?!
        # TODO decorator!!
        # TODO (utils.get_dataframe, ['messages']), maybe make dataframes recursively
        return [
            (utils.decode_text, None), (utils.get_dataframe, ['messages']),
            (self.set_date_as_index, None), (self.add_partner_column, None)
        ]

    @staticmethod
    def set_date_as_index(data: pd.DataFrame) -> pd.DataFrame:
        date_series = data.timestamp_ms.apply(utils.ts_to_date)
        return data.set_index(date_series).iloc[::-1]

    @staticmethod
    def add_partner_column(data: pd.DataFrame) -> pd.DataFrame:
        data['partner'] = data.title
        return data

    # @property
    # def names(self):
    #     # TODO names? bad name?! name vs participants
    #     # TODO symetricallity should be kept with Friends and all tabular data
    #     try:
    #         return pd.DataFrame(self.participants)[0]
    #     except KeyError:
    #         return pd.Series({0: 'Facebook User'})
    #
    # @property
    # def participants(self):
    #     # TODO p
    #     participants = self.decoded.get('participants')
    #     return [p.get('name') for p in participants if p.get('name')]
    #
    # @property
    # def title(self):
    #     return self.decoded.get('title')
    #
    # @property
    # def ttype(self):
    #     # TODO name bad
    #     return self.decoded.get('thread_type')
    #
    # @property
    # def messages_dir(self):
    #     # TODO json dir
    #     thread_path = self.decoded.get('thread_path')
    #     if not thread_path.startswith('inbox/'):
    #         raise ValueError('Field `thread_path` should start with `inbox/`.')
    #     return thread_path.split('inbox/')[1]
    #
    # @property
    # def media_dir(self):
    #     # TODO name should be ok
    #     for media in utils.MEDIA_DIRS:
    #         if media in self._df.columns:
    #             media_in_msg = list(self._df[media][self._df[media].notnull()])
    #             uri = media_in_msg[0][0].get('uri')
    #             return os.path.dirname(os.path.dirname(uri)).split('inbox/')[1]

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
