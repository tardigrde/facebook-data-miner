from miner.FacebookData import TabularFacebookData, FacebookData
from miner.Individual import Individual
from miner import utils
import pandas as pd
from typing import Union, List, Dict, Callable, Any


# TODO get_people is not implemented yet
class Friends:
    sub_path = '/friends'

    def __init__(self, path: str, reader: Callable = None, processors: List[Callable] = None) -> None:
        self.path = self.make_path(path)
        self._reader = reader
        self._processors = processors

        fb = FacebookData(self.path)
        self._data = fb.get_data(reader=self.reader, processors=self.processors)

    @property
    def data(self):
        return self._data

    @property
    def reader(self):
        return utils.read_json if not self._reader else self._reader

    @property
    def processors(self) -> Any:
        # TODO maybe a better solution for passing in args and kwargs?!
        # TODO decorator!!
        if self._processors:
            return self._processors
        return [(utils.decode_text, None), (utils.get_dataframe, ['friends'])]

    def make_path(self, path):
        return path + self.sub_path + '/friends.json'

# TODO all the other jsons whic are in friends as subclasses

# class Friends(TabularFacebookData):
#     """
#     Class for storing data in friends.json
#     """
#
#     def __init__(self, *args):
#         super().__init__(*args)
#         self.to_df('friends')
#
#     def get_people(self, name=None):
#         # TODO make this iterable
#         names = {}
#         for full_name, compact in zip(self.names, self.compact_names):
#             if name is not None and name != full_name:  # filtering for name
#                 continue
#             names[full_name] = Individual(
#                 name=full_name,
#                 compact=compact,
#                 friend=True,
#             )
#         return names
#
#     @property
#     def names(self):
#         return self.df.name
